{
  "timestamp": "20260507_130540",
  "artifacts": {
    "json": "results/swine_parallel_pilot/swine_parallel_pilot_20260507_130540.json",
    "csv": "results/swine_parallel_pilot/swine_parallel_pilot_20260507_130540.csv",
    "summary": "results/swine_parallel_pilot/swine_parallel_pilot_summary_20260507_130540.json"
  },
  "summary": {
    "timestamp": "20260507_130542",
    "sample_count": 16,
    "score_avg": 78.69,
    "score_min": 65.0,
    "score_max": 90.0,
    "pass_count": 4,
    "review_count": 11,
    "reject_count": 1,
    "fatal_count": 1,
    "specific_dose_count": 1,
    "specific_withdrawal_count": 0,
    "answer_anchor_avg": 3.06,
    "elapsed_avg_seconds": 63.6,
    "elapsed_p50_seconds": 57.15,
    "elapsed_p90_seconds": 107.77,
    "parallel": 8,
    "wall_seconds": 203.93,
    "throughput_cases_per_minute": 4.71
  },
  "fallback_events": [
    {
      "case_id": "SWINE10-005",
      "stage": "answer",
      "attempts": [
        {
          "model": "hunyuan-turbos-20250926",
          "success": true,
          "elapsed_seconds": 14.03,
          "attempts": 1,
          "api_key_fingerprint": "8798281415b6",
          "error_category": "",
          "error": "",
          "parsed_json": false,
          "has_required_json": false,
          "usage": {
            "input_tokens": 3287,
            "output_tokens": 547,
            "total_tokens": 3834,
            "cached_input_tokens": 0,
            "reasoning_tokens": 0
          },
          "cost": {
            "input_cost": 0.00263,
            "cached_input_cost": 0.0,
            "output_cost": 0.001094,
            "total_cost": 0.003724,
            "currency": "CNY"
          }
        },
        {
          "model": "ERNIE-4.5-Turbo-32K",
          "success": true,
          "elapsed_seconds": 33.46,
          "attempts": 1,
          "api_key_fingerprint": "8cb453872788",
          "error_category": "",
          "error": "",
          "parsed_json": true,
          "has_required_json": true,
          "usage": {
            "input_tokens": 3429,
            "output_tokens": 780,
            "total_tokens": 4209,
            "cached_input_tokens": 0,
            "reasoning_tokens": 0
          },
          "cost": {
            "input_cost": 0.002743,
            "cached_input_cost": 0.0,
            "output_cost": 0.002496,
            "total_cost": 0.005239,
            "currency": "CNY"
          }
        }
      ]
    },
    {
      "case_id": "SWINE10-008",
      "stage": "judge",
      "attempts": [
        {
          "model": "ERNIE-4.5-Turbo-32K",
          "success": true,
          "elapsed_seconds": 46.66,
          "attempts": 1,
          "api_key_fingerprint": "344c9291a027",
          "error_category": "",
          "error": "",
          "parsed_json": true,
          "has_required_json": false,
          "usage": {
            "input_tokens": 3781,
            "output_tokens": 1130,
            "total_tokens": 4911,
            "cached_input_tokens": 0,
            "reasoning_tokens": 0
          },
          "cost": {
            "input_cost": 0.003025,
            "cached_input_cost": 0.0,
            "output_cost": 0.003616,
            "total_cost": 0.006641,
            "currency": "CNY"
          }
        },
        {
          "model": "hunyuan-2.0-instruct-20251111",
          "success": true,
          "elapsed_seconds": 11.96,
          "attempts": 1,
          "api_key_fingerprint": "344c9291a027",
          "error_category": "",
          "error": "",
          "parsed_json": true,
          "has_required_json": true,
          "usage": {
            "input_tokens": 3475,
            "output_tokens": 335,
            "total_tokens": 3810,
            "cached_input_tokens": 0,
            "reasoning_tokens": 0
          },
          "cost": {
            "input_cost": 0.015637,
            "cached_input_cost": 0.0,
            "output_cost": 0.003729,
            "total_cost": 0.019366,
            "currency": "CNY"
          }
        }
      ]
    },
    {
      "case_id": "SWINE30-DIS-001",
      "stage": "answer",
      "attempts": [
        {
          "model": "hunyuan-turbos-20250926",
          "success": true,
          "elapsed_seconds": 9.28,
          "attempts": 1,
          "api_key_fingerprint": "7b8b49842efc",
          "error_category": "",
          "error": "",
          "parsed_json": true,
          "has_required_json": false,
          "usage": {
            "input_tokens": 3279,
            "output_tokens": 587,
            "total_tokens": 3866,
            "cached_input_tokens": 0,
            "reasoning_tokens": 0
          },
          "cost": {
            "input_cost": 0.002623,
            "cached_input_cost": 0.0,
            "output_cost": 0.001174,
            "total_cost": 0.003797,
            "currency": "CNY"
          }
        },
        {
          "model": "ERNIE-4.5-Turbo-32K",
          "success": true,
          "elapsed_seconds": 93.55,
          "attempts": 1,
          "api_key_fingerprint": "13cbb25a8cc3",
          "error_category": "",
          "error": "",
          "parsed_json": true,
          "has_required_json": true,
          "usage": {
            "input_tokens": 3468,
            "output_tokens": 1037,
            "total_tokens": 4505,
            "cached_input_tokens": 0,
            "reasoning_tokens": 0
          },
          "cost": {
            "input_cost": 0.002774,
            "cached_input_cost": 0.0,
            "output_cost": 0.003318,
            "total_cost": 0.006093,
            "currency": "CNY"
          }
        }
      ]
    },
    {
      "case_id": "SWINE30-DIS-003",
      "stage": "judge",
      "attempts": [
        {
          "model": "ERNIE-4.5-Turbo-32K",
          "success": true,
          "elapsed_seconds": 43.08,
          "attempts": 1,
          "api_key_fingerprint": "8798281415b6",
          "error_category": "",
          "error": "",
          "parsed_json": true,
          "has_required_json": false,
          "usage": {
            "input_tokens": 3911,
            "output_tokens": 1103,
            "total_tokens": 5014,
            "cached_input_tokens": 0,
            "reasoning_tokens": 0
          },
          "cost": {
            "input_cost": 0.003129,
            "cached_input_cost": 0.0,
            "output_cost": 0.00353,
            "total_cost": 0.006658,
            "currency": "CNY"
          }
        },
        {
          "model": "hunyuan-2.0-instruct-20251111",
          "success": true,
          "elapsed_seconds": 11.24,
          "attempts": 1,
          "api_key_fingerprint": "50d7546f044f",
          "error_category": "",
          "error": "",
          "parsed_json": true,
          "has_required_json": true,
          "usage": {
            "input_tokens": 3692,
            "output_tokens": 383,
            "total_tokens": 4075,
            "cached_input_tokens": 0,
            "reasoning_tokens": 0
          },
          "cost": {
            "input_cost": 0.016614,
            "cached_input_cost": 0.0,
            "output_cost": 0.004263,
            "total_cost": 0.020877,
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
