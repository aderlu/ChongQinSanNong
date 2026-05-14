{
  "timestamp": "20260507_124018",
  "artifacts": {
    "json": "results/swine_parallel_pilot/swine_parallel_pilot_20260507_124018.json",
    "csv": "results/swine_parallel_pilot/swine_parallel_pilot_20260507_124018.csv",
    "summary": "results/swine_parallel_pilot/swine_parallel_pilot_summary_20260507_124018.json"
  },
  "summary": {
    "timestamp": "20260507_124019",
    "sample_count": 30,
    "score_avg": 80.8,
    "score_min": 70.0,
    "score_max": 92.0,
    "pass_count": 15,
    "review_count": 14,
    "reject_count": 1,
    "fatal_count": 1,
    "specific_dose_count": 0,
    "specific_withdrawal_count": 0,
    "answer_anchor_avg": 3.27,
    "elapsed_avg_seconds": 77.0,
    "elapsed_p50_seconds": 55.74,
    "elapsed_p90_seconds": 175.51,
    "parallel": 8,
    "wall_seconds": 363.55,
    "throughput_cases_per_minute": 4.95
  },
  "fallback_events": [
    {
      "case_id": "SWINE30-DIS-007",
      "stage": "answer",
      "attempts": [
        {
          "model": "hunyuan-turbos-20250926",
          "success": true,
          "elapsed_seconds": 11.8,
          "attempts": 1,
          "api_key_fingerprint": "8a1384ec8046",
          "error_category": "",
          "error": "",
          "parsed_json": true,
          "has_required_json": false,
          "usage": {
            "input_tokens": 3299,
            "output_tokens": 641,
            "total_tokens": 3940,
            "cached_input_tokens": 0,
            "reasoning_tokens": 0
          },
          "cost": {
            "input_cost": 0.002639,
            "cached_input_cost": 0.0,
            "output_cost": 0.001282,
            "total_cost": 0.003921,
            "currency": "CNY"
          }
        },
        {
          "model": "ERNIE-4.5-Turbo-32K",
          "success": true,
          "elapsed_seconds": 39.84,
          "attempts": 1,
          "api_key_fingerprint": "d86bf62fd68d",
          "error_category": "",
          "error": "",
          "parsed_json": true,
          "has_required_json": true,
          "usage": {
            "input_tokens": 3483,
            "output_tokens": 985,
            "total_tokens": 4468,
            "cached_input_tokens": 0,
            "reasoning_tokens": 0
          },
          "cost": {
            "input_cost": 0.002786,
            "cached_input_cost": 0.0,
            "output_cost": 0.003152,
            "total_cost": 0.005938,
            "currency": "CNY"
          }
        }
      ]
    },
    {
      "case_id": "SWINE30-DIS-007",
      "stage": "judge",
      "attempts": [
        {
          "model": "ERNIE-4.5-Turbo-32K",
          "success": true,
          "elapsed_seconds": 40.46,
          "attempts": 1,
          "api_key_fingerprint": "13cbb25a8cc3",
          "error_category": "",
          "error": "",
          "parsed_json": true,
          "has_required_json": false,
          "usage": {
            "input_tokens": 4030,
            "output_tokens": 1142,
            "total_tokens": 5172,
            "cached_input_tokens": 0,
            "reasoning_tokens": 0
          },
          "cost": {
            "input_cost": 0.003224,
            "cached_input_cost": 0.0,
            "output_cost": 0.003654,
            "total_cost": 0.006878,
            "currency": "CNY"
          }
        },
        {
          "model": "hunyuan-2.0-instruct-20251111",
          "success": true,
          "elapsed_seconds": 76.33,
          "attempts": 2,
          "api_key_fingerprint": "1e8b06b345f7",
          "error_category": "",
          "error": "",
          "parsed_json": true,
          "has_required_json": true,
          "usage": {
            "input_tokens": 3754,
            "output_tokens": 504,
            "total_tokens": 4258,
            "cached_input_tokens": 0,
            "reasoning_tokens": 0
          },
          "cost": {
            "input_cost": 0.016893,
            "cached_input_cost": 0.0,
            "output_cost": 0.00561,
            "total_cost": 0.022503,
            "currency": "CNY"
          }
        }
      ]
    },
    {
      "case_id": "SWINE30-DIS-013",
      "stage": "judge",
      "attempts": [
        {
          "model": "ERNIE-4.5-Turbo-32K",
          "success": false,
          "elapsed_seconds": 125.35,
          "attempts": 2,
          "api_key_fingerprint": "8798281415b6",
          "error_category": "other",
          "error": "Connection error.",
          "parsed_json": false,
          "has_required_json": false,
          "usage": {},
          "cost": {}
        },
        {
          "model": "hunyuan-2.0-instruct-20251111",
          "success": true,
          "elapsed_seconds": 34.48,
          "attempts": 1,
          "api_key_fingerprint": "8cb453872788",
          "error_category": "",
          "error": "",
          "parsed_json": true,
          "has_required_json": true,
          "usage": {
            "input_tokens": 3716,
            "output_tokens": 455,
            "total_tokens": 4171,
            "cached_input_tokens": 0,
            "reasoning_tokens": 0
          },
          "cost": {
            "input_cost": 0.016722,
            "cached_input_cost": 0.0,
            "output_cost": 0.005064,
            "total_cost": 0.021786,
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
          "elapsed_seconds": 63.94,
          "attempts": 1,
          "api_key_fingerprint": "8a1384ec8046",
          "error_category": "",
          "error": "",
          "parsed_json": true,
          "has_required_json": false,
          "usage": {
            "input_tokens": 4088,
            "output_tokens": 1110,
            "total_tokens": 5198,
            "cached_input_tokens": 0,
            "reasoning_tokens": 0
          },
          "cost": {
            "input_cost": 0.00327,
            "cached_input_cost": 0.0,
            "output_cost": 0.003552,
            "total_cost": 0.006822,
            "currency": "CNY"
          }
        },
        {
          "model": "hunyuan-2.0-instruct-20251111",
          "success": true,
          "elapsed_seconds": 13.55,
          "attempts": 1,
          "api_key_fingerprint": "344c9291a027",
          "error_category": "",
          "error": "",
          "parsed_json": true,
          "has_required_json": true,
          "usage": {
            "input_tokens": 3749,
            "output_tokens": 318,
            "total_tokens": 4067,
            "cached_input_tokens": 0,
            "reasoning_tokens": 0
          },
          "cost": {
            "input_cost": 0.016871,
            "cached_input_cost": 0.0,
            "output_cost": 0.003539,
            "total_cost": 0.02041,
            "currency": "CNY"
          }
        }
      ]
    },
    {
      "case_id": "SWINE30-DIS-018",
      "stage": "judge",
      "attempts": [
        {
          "model": "ERNIE-4.5-Turbo-32K",
          "success": true,
          "elapsed_seconds": 69.74,
          "attempts": 1,
          "api_key_fingerprint": "fb3e9e31f56d",
          "error_category": "",
          "error": "",
          "parsed_json": true,
          "has_required_json": false,
          "usage": {
            "input_tokens": 4300,
            "output_tokens": 1112,
            "total_tokens": 5412,
            "cached_input_tokens": 0,
            "reasoning_tokens": 0
          },
          "cost": {
            "input_cost": 0.00344,
            "cached_input_cost": 0.0,
            "output_cost": 0.003558,
            "total_cost": 0.006998,
            "currency": "CNY"
          }
        },
        {
          "model": "hunyuan-2.0-instruct-20251111",
          "success": true,
          "elapsed_seconds": 10.67,
          "attempts": 1,
          "api_key_fingerprint": "13cbb25a8cc3",
          "error_category": "",
          "error": "",
          "parsed_json": true,
          "has_required_json": true,
          "usage": {
            "input_tokens": 4014,
            "output_tokens": 322,
            "total_tokens": 4336,
            "cached_input_tokens": 0,
            "reasoning_tokens": 0
          },
          "cost": {
            "input_cost": 0.018063,
            "cached_input_cost": 0.0,
            "output_cost": 0.003584,
            "total_cost": 0.021647,
            "currency": "CNY"
          }
        }
      ]
    }
  ],
  "error_categories": [
    "other"
  ],
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
  "api_key_recommendation": "review_key_capacity"
}
