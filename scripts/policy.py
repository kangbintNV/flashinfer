"""Bounded analysis retry; unknown never grants a CPU exemption."""
import json


def parse_response(body):
    try:
        data = json.loads(body[:100001])
        choice = data['choices'][0]
        if choice.get('finish_reason') not in (None, 'stop'):
            raise ValueError('Inference Hub response was incomplete')
        content = choice['message']['content']
        if not isinstance(content, str) or len(content) > 50000:
            raise ValueError('Inference Hub returned invalid content')
        result = json.loads(content)
        if not isinstance(result, dict):
            raise ValueError('Inference Hub returned a non-object response')
        return result
    except (KeyError, IndexError, TypeError, json.JSONDecodeError, UnicodeError) as error:
        raise ValueError('Inference Hub returned invalid JSON') from error


def analyze_with_retry(analyze):
    attempts = []
    for effort in ('default', 'minimal'):
        try:
            result = analyze(effort)
            if result['classification'] not in ('gpu_required', 'cpu_only', 'docs_only'):
                raise ValueError(result.get('reason') or 'Unable to determine GPU impact')
        except ValueError as error:
            attempts.append({'effort': effort, 'success': False, 'error': str(error)})
        else:
            attempts.append({'effort': effort, 'success': True, 'impact': result})
            return result, attempts
    return {'classification': 'unknown', 'reason': attempts[-1]['error'], 'evidence_paths': [], 'case_gap': '', 'targets': []}, attempts
