"""Replay a frozen final request through the unmodified parser while capturing bytes."""
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sys
import time
import urllib.error
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent / 'pr_checks'))
import ai_test_scope as scope

ROOT = Path(__file__).resolve().parents[1]
LEGACY_CAP = 100_001
CAPTURE_CAP = 1_000_000


def parse_error(error):
    return {key: getattr(error, key) for key in ('msg', 'pos', 'lineno', 'colno') if hasattr(error, key)}


def redact(value, secrets):
    if isinstance(value, str):
        return scope._redact_credentials(value, secrets)
    if isinstance(value, list):
        return [redact(item, secrets) for item in value]
    if isinstance(value, dict):
        return {key: redact(item, secrets) for key, item in value.items()}
    return value


def analyze_body(body):
    result = {'body_bytes': len(body), 'legacy_read_cap_hit': len(body) > LEGACY_CAP}
    try:
        data = json.loads(body)
    except (ValueError, UnicodeError) as error:
        result.update(category='invalid_api_json', parse_error=parse_error(error))
        return result
    try:
        json.loads(body[:LEGACY_CAP])
    except (ValueError, UnicodeError) as error:
        result.update(category='client_read_truncation', parse_error=parse_error(error))
        return result
    if isinstance(data, dict):
        result['api_keys'] = list(data)
        result['usage'] = data.get('usage')
    try:
        choice = data['choices'][0]
        finish = choice.get('finish_reason')
        result['finish_reason'] = finish
        if finish not in (None, 'stop'):
            result['category'] = 'output_token_limit' if finish == 'length' else 'other_incomplete_response'
            return result
        content = choice['message']['content']
    except (KeyError, IndexError, TypeError, AttributeError) as error:
        result.update(category='invalid_api_envelope', exception_type=type(error).__name__)
        return result
    if not isinstance(content, str):
        result.update(category='invalid_content_type', content_type=type(content).__name__)
        return result
    result.update(content_chars=len(content), content_head=content[:500], content_tail=content[-500:])
    try:
        value = json.loads(content)
        result['category'] = 'valid_json' if isinstance(value, dict) else 'non_object_json'
        return result
    except ValueError as error:
        result.update(category='model_content_json_syntax', parse_error=parse_error(error))
    fenced = re.fullmatch(r'\s*```(?:json)?[ \t]*\r?\n([\s\S]*?)\r?\n```\s*', content, re.IGNORECASE)
    if fenced:
        try:
            value = json.loads(fenced.group(1))
            if isinstance(value, dict):
                result.update(category='json_code_fence', fence_parsing_would_succeed=True)
        except ValueError:
            pass
    return result


class CapturedResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def main():
    n = int(os.environ['CASE_ID'])
    frozen = json.loads((ROOT / f'inputs/{n}.json').read_text())
    model = scope.InferenceHub()
    model.deadline = time.monotonic() + 360
    output = ROOT / f'reports/{n}/result.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    secrets = tuple(value for value in (model.api_key, os.getenv('GH_TOKEN'), os.getenv('GITHUB_TOKEN')) if value)
    report = {'metadata': frozen['metadata'], 'model': model.model, 'responses': []}

    def save():
        output.write_text(json.dumps(redact(report, secrets), ensure_ascii=True))

    real_open = scope.urllib.request.urlopen

    def record(request, timeout):
        start = time.monotonic()
        payload = json.loads(request.data)
        observed_hash = hashlib.sha256(request.data).hexdigest()
        assert observed_hash == frozen['metadata']['payload_sha256'], 'Payload differs from frozen original request'
        entry = {'request_sha256': observed_hash, 'max_tokens': payload['max_tokens'], 'http_timeout_seconds': timeout}
        report['responses'].append(entry)
        try:
            with real_open(request, timeout=timeout) as response:
                body = response.read(CAPTURE_CAP + 1)
                entry['http_status'] = response.status
                allowed = ('content-type', 'content-length', 'x-request-id', 'request-id', 'x-ms-request-id', 'x-amzn-requestid')
                entry['response_headers'] = {key: response.headers[key] for key in allowed if response.headers.get(key)}
        except urllib.error.HTTPError as error:
            body = error.read(CAPTURE_CAP + 1)
            entry.update(http_status=error.code, raw_body_utf8=body.decode('utf-8', 'replace'), seconds=round(time.monotonic() - start, 3))
            save()
            raise urllib.error.HTTPError(error.url, error.code, error.reason, error.headers, io.BytesIO(body)) from None
        except Exception as error:
            entry.update(transport_exception=type(error).__name__, seconds=round(time.monotonic() - start, 3))
            save()
            raise
        entry.update(seconds=round(time.monotonic() - start, 3), capture_cap_hit=len(body) > CAPTURE_CAP, response_sha256=hashlib.sha256(body).hexdigest(), raw_body_utf8=body.decode('utf-8', 'replace'), diagnosis=analyze_body(body))
        save()
        return CapturedResponse(body)

    try:
        with patch.object(scope.urllib.request, 'urlopen', side_effect=record):
            result = model.complete(frozen['context'], frozen['task'])
        report.update(legacy_result='success', result=result)
    except Exception as error:
        report.update(legacy_result='failure', legacy_error=str(error), exception_type=type(error).__name__)
        if error.__cause__:
            report['exception_cause'] = {'type': type(error.__cause__).__name__, **parse_error(error.__cause__)}
    save()
    categories = [entry.get('diagnosis', {}).get('category') for entry in report['responses']]
    summary = f"## Original PR #{n} / demo #{frozen['metadata']['demo_number']}\n\nOriginal error: `{frozen['metadata']['original_error']}`.\n\nFresh replay, same frozen payload, unchanged 4000-token limit and parser.\n\nLegacy parser: **{report['legacy_result']}**. Diagnosis: `{categories}`.\n\nFull redacted response and parse position are in the artifact. Historical failure raw bodies were not retained; fresh replay is reproduction evidence.\n"
    with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as stream:
        stream.write(summary)
    print(json.dumps({'pr': n, 'legacy_result': report['legacy_result'], 'diagnosis': categories}))


if __name__ == '__main__':
    main()
