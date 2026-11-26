import json
import unittest
from policy import analyze_with_retry, parse_response


def impact(kind):
    return {'classification': kind, 'reason': 'test', 'targets': []}


class RetryTests(unittest.TestCase):
    def replay(self, outputs):
        self.efforts = []
        def analyze(effort):
            self.efforts.append(effort)
            value = outputs[len(self.efforts)-1]
            if isinstance(value, Exception):
                raise value
            return value
        return analyze_with_retry(analyze)

    def test_valid_cpu_does_not_retry(self):
        value, attempts = self.replay([impact('cpu_only')])
        self.assertEqual((value['classification'], self.efforts), ('cpu_only', ['default']))

    def test_valid_gpu_requires_bot_without_retry(self):
        value, attempts = self.replay([impact('gpu_required')])
        self.assertEqual((value['classification'], self.efforts), ('gpu_required', ['default']))

    def test_failed_default_can_recover_cpu(self):
        value, attempts = self.replay([ValueError('invalid JSON'), impact('cpu_only')])
        self.assertEqual((value['classification'], self.efforts), ('cpu_only', ['default', 'minimal']))
        self.assertEqual(attempts[0]['error'], 'invalid JSON')

    def test_unknown_retries_once_and_never_grants_exemption(self):
        value, attempts = self.replay([impact('unknown'), impact('unknown')])
        self.assertEqual((value['classification'], self.efforts), ('unknown', ['default', 'minimal']))
        self.assertTrue(all(not a['success'] for a in attempts))

    def test_two_failures_stop_and_preserve_causes(self):
        value, attempts = self.replay([ValueError('incomplete'), ValueError('uninspected target')])
        self.assertEqual(value['classification'], 'unknown')
        self.assertEqual([a['error'] for a in attempts], ['incomplete', 'uninspected target'])

    def test_incomplete_finish_is_rejected_even_with_valid_content(self):
        body = json.dumps({'choices':[{'finish_reason':'length','message':{'content':'{}'}}]}).encode()
        with self.assertRaisesRegex(ValueError, 'incomplete'):
            parse_response(body)

    def test_json_fence_is_not_silently_accepted(self):
        body = json.dumps({'choices':[{'finish_reason':'stop','message':{'content':'```json\n{}\n```'}}]}).encode()
        with self.assertRaisesRegex(ValueError, 'invalid JSON'):
            parse_response(body)


if __name__ == '__main__':
    unittest.main()
