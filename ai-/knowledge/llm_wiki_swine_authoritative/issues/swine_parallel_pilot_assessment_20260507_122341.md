{
  "timestamp": "20260507_122341",
  "artifacts": {
    "json": "results/swine_parallel_pilot/swine_parallel_pilot_20260507_122341.json",
    "csv": "results/swine_parallel_pilot/swine_parallel_pilot_20260507_122341.csv",
    "summary": "results/swine_parallel_pilot/swine_parallel_pilot_summary_20260507_122341.json"
  },
  "summary": {
    "timestamp": "20260507_122342",
    "sample_count": 30,
    "score_avg": 78.93,
    "score_min": 65.0,
    "score_max": 89.0,
    "pass_count": 14,
    "review_count": 14,
    "reject_count": 2,
    "fatal_count": 1,
    "specific_dose_count": 0,
    "specific_withdrawal_count": 0,
    "answer_anchor_avg": 2.8,
    "elapsed_avg_seconds": 64.37,
    "elapsed_p50_seconds": 55.74,
    "elapsed_p90_seconds": 96.63,
    "parallel": 6,
    "wall_seconds": 396.9,
    "throughput_cases_per_minute": 4.54
  },
  "fallback_events": [
    {
      "case_id": "SWINE30-DIS-001",
      "stage": "judge",
      "attempts": [
        {
          "model": "ERNIE-4.5-Turbo-32K",
          "success": true,
          "elapsed_seconds": 46.0,
          "attempts": 1,
          "api_key_fingerprint": "fb3e9e31f56d",
          "error_category": "",
          "error": "",
          "parsed_json": true,
          "has_required_json": false,
          "usage": {
            "input_tokens": 4011,
            "output_tokens": 1119,
            "total_tokens": 5130,
            "cached_input_tokens": 0,
            "reasoning_tokens": 0
          },
          "cost": {
            "input_cost": 0.003209,
            "cached_input_cost": 0.0,
            "output_cost": 0.003581,
            "total_cost": 0.00679,
            "currency": "CNY"
          }
        },
        {
          "model": "hunyuan-2.0-instruct-20251111",
          "success": true,
          "elapsed_seconds": 19.69,
          "attempts": 1,
          "api_key_fingerprint": "7b8b49842efc",
          "error_category": "",
          "error": "",
          "parsed_json": true,
          "has_required_json": true,
          "usage": {
            "input_tokens": 3796,
            "output_tokens": 594,
            "total_tokens": 4390,
            "cached_input_tokens": 0,
            "reasoning_tokens": 0
          },
          "cost": {
            "input_cost": 0.017082,
            "cached_input_cost": 0.0,
            "output_cost": 0.006611,
            "total_cost": 0.023693,
            "currency": "CNY"
          }
        }
      ]
    },
    {
      "case_id": "SWINE30-DIS-005",
      "stage": "judge",
      "attempts": [
        {
          "model": "ERNIE-4.5-Turbo-32K",
          "success": true,
          "elapsed_seconds": 43.64,
          "attempts": 1,
          "api_key_fingerprint": "75595635c32e",
          "error_category": "",
          "error": "",
          "parsed_json": true,
          "has_required_json": false,
          "usage": {
            "input_tokens": 4190,
            "output_tokens": 1143,
            "total_tokens": 5333,
            "cached_input_tokens": 0,
            "reasoning_tokens": 0
          },
          "cost": {
            "input_cost": 0.003352,
            "cached_input_cost": 0.0,
            "output_cost": 0.003658,
            "total_cost": 0.00701,
            "currency": "CNY"
          }
        },
        {
          "model": "hunyuan-2.0-instruct-20251111",
          "success": true,
          "elapsed_seconds": 14.44,
          "attempts": 1,
          "api_key_fingerprint": "089989b20091",
          "error_category": "",
          "error": "",
          "parsed_json": true,
          "has_required_json": true,
          "usage": {
            "input_tokens": 3972,
            "output_tokens": 447,
            "total_tokens": 4419,
            "cached_input_tokens": 0,
            "reasoning_tokens": 0
          },
          "cost": {
            "input_cost": 0.017874,
            "cached_input_cost": 0.0,
            "output_cost": 0.004975,
            "total_cost": 0.022849,
            "currency": "CNY"
          }
        }
      ]
    },
    {
      "case_id": "SWINE30-DIS-016",
      "stage": "judge",
      "attempts": [
        {
          "model": "ERNIE-4.5-Turbo-32K",
          "success": true,
          "elapsed_seconds": 47.02,
          "attempts": 1,
          "api_key_fingerprint": "d86bf62fd68d",
          "error_category": "",
          "error": "",
          "parsed_json": true,
          "has_required_json": false,
          "usage": {
            "input_tokens": 4066,
            "output_tokens": 1106,
            "total_tokens": 5172,
            "cached_input_tokens": 0,
            "reasoning_tokens": 0
          },
          "cost": {
            "input_cost": 0.003253,
            "cached_input_cost": 0.0,
            "output_cost": 0.003539,
            "total_cost": 0.006792,
            "currency": "CNY"
          }
        },
        {
          "model": "hunyuan-2.0-instruct-20251111",
          "success": true,
          "elapsed_seconds": 12.7,
          "attempts": 1,
          "api_key_fingerprint": "1e8b06b345f7",
          "error_category": "",
          "error": "",
          "parsed_json": true,
          "has_required_json": true,
          "usage": {
            "input_tokens": 3822,
            "output_tokens": 469,
            "total_tokens": 4291,
            "cached_input_tokens": 0,
            "reasoning_tokens": 0
          },
          "cost": {
            "input_cost": 0.017199,
            "cached_input_cost": 0.0,
            "output_cost": 0.00522,
            "total_cost": 0.022419,
            "currency": "CNY"
          }
        }
      ]
    },
    {
      "case_id": "SWINE30-DIS-017",
      "stage": "answer",
      "attempts": [
        {
          "model": "hunyuan-turbos-20250926",
          "success": true,
          "elapsed_seconds": 14.62,
          "attempts": 1,
          "api_key_fingerprint": "089989b20091",
          "error_category": "",
          "error": "",
          "parsed_json": true,
          "has_required_json": false,
          "usage": {
            "input_tokens": 3293,
            "output_tokens": 1100,
            "total_tokens": 4393,
            "cached_input_tokens": 0,
            "reasoning_tokens": 0
          },
          "cost": {
            "input_cost": 0.002634,
            "cached_input_cost": 0.0,
            "output_cost": 0.0022,
            "total_cost": 0.004834,
            "currency": "CNY"
          }
        },
        {
          "model": "ERNIE-4.5-Turbo-32K",
          "success": true,
          "elapsed_seconds": 40.44,
          "attempts": 1,
          "api_key_fingerprint": "75595635c32e",
          "error_category": "",
          "error": "",
          "parsed_json": true,
          "has_required_json": true,
          "usage": {
            "input_tokens": 3464,
            "output_tokens": 1122,
            "total_tokens": 4586,
            "cached_input_tokens": 0,
            "reasoning_tokens": 0
          },
          "cost": {
            "input_cost": 0.002771,
            "cached_input_cost": 0.0,
            "output_cost": 0.00359,
            "total_cost": 0.006362,
            "currency": "CNY"
          }
        }
      ]
    }
  ],
  "error_categories": [],
  "key_fingerprints_used_count": 19,
  "key_fingerprints_used": [
    "089989b20091",
    "13cbb25a8cc3",
    "1e8b06b345f7",
    "232377ce6842",
    "344c9291a027",
    "408f1ccf2d63",
    "4ae0cab1a311",
    "50d7546f044f",
    "6bb171346afa",
    "75595635c32e",
    "7b8b49842efc",
    "8798281415b6",
    "8a1384ec8046",
    "8cb453872788",
    "993313a8c81a",
    "ca6a04186520",
    "d242c7423361",
    "d86bf62fd68d",
    "fb3e9e31f56d"
  ],
  "api_key_recommendation": "no_new_keys_needed"
}
