---
type: synthesis
page_id: swine_textbook_pages_1_200_crosscutting_digest
title: Diseases of Swine 11e pages 1-200 crosscutting digest
category: diagnostic_quality
derived: true
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, audit_only, source_digest]
sources:
  - SRC-0003
  - SRC-0008
  - SRC-0009
  - SRC-0010
  - SRC-0011
  - SRC-0012
  - SRC-0013
raw_source: raw/md/1-200.md
---

# Diseases of Swine 11e pages 1-200 crosscutting digest

This page summarizes the operational knowledge extracted from the first 200 pages of *Diseases of Swine, 11th Edition* as represented in `raw/md/1-200.md`. It is a derived synthesis page, not a substitute for the underlying source pages. Use it to improve swine disease case generation, sampling recommendations, diagnosis evaluation, biosecurity boundaries, and drug-use safety checks.

## Coverage assessment

The first 200 pages are primarily general veterinary practice and herd-health chapters rather than single-disease chapters. They do not fully solve disease-specific gaps such as clinical signs, lesions, or differential diagnosis for individual diseases. They do, however, strongly support crosscutting rules that are currently needed by the wiki:

- herd evaluation and field investigation structure
- diagnostic question framing
- representative animal selection
- antemortem and postmortem sample selection
- necropsy workflow and safety
- diagnostic evidence and causality limits
- disease control, biosecurity, and movement-risk reasoning
- drug therapy objectives, routes, regulation, withdrawal, and prudent use
- anesthesia/surgical context boundaries

## Knowledge absorbed from pages 1-200

### 1. Herd evaluation should be structured before diagnosis

Case generation and evaluation should not jump directly from one symptom to one disease. A high-quality swine case should include enough herd context to support a herd-level diagnostic question:

- production stage and group size
- onset, duration, spread, morbidity, and mortality pattern
- recent movements, feed changes, medication, vaccination, and management changes
- building, pen, and individual pig observations
- records, benchmarks, and production-impact context

Dataset impact: generated `user_query` should contain a realistic herd context, not only a symptom list. Judge scoring should penalize answers that ignore the herd-level pattern when the question clearly describes group disease.

### 2. Diagnosis should be framed as a process, not a single unsupported label

The diagnostic chapters emphasize that clinical observation, history, lesions, and lab testing must be interpreted together. A generated answer should:

- name the most likely disease when justified
- explain why the scenario supports it
- state important differential diagnoses when signs overlap
- recommend sampling/testing when clinical signs alone are insufficient
- avoid pretending that one isolated sign confirms a disease

Dataset impact: `diagnosis` should connect disease, signs, stage, herd pattern, and uncertainty. `final_label=pass` should require the diagnosis to be consistent with the target disease and to avoid overclaiming.

### 3. Sample selection is part of the diagnostic answer

The sample-selection content can fill a major current wiki gap. Good swine QA should not merely say "send samples"; it should choose samples based on the syndrome and diagnostic question.

General rules:

- sample animals that best represent the active problem
- prefer untreated or early untreated cases when possible
- match sample type to syndrome and lesion distribution
- collect adequate history with submissions
- use postmortem samples when deaths or lesions are central to the question
- preserve tissue appropriately for histopathology, culture, PCR, or toxicology as needed

Dataset impact: answers should be rewarded for syndrome-appropriate sampling. Generic "send to lab" without sample type should be a lower-quality answer for formal training data.

### 4. Necropsy and postmortem evidence need explicit boundaries

The necropsy sections support stronger evaluation of acute death, septicemia, respiratory disease, digestive disease, neurologic disease, reproductive failure, lameness, and toxin scenarios.

Useful generated-answer patterns:

- acute death: include postmortem exam and tissue sampling before disposal when safe and legal
- respiratory disease: include lung and respiratory tract sampling when lesions are relevant
- digestive disease: include intestinal contents, feces, and affected intestinal segments when relevant
- reproductive failure: include fetuses, placenta, and sow/gilt samples when relevant
- neurologic signs: include CNS sampling only with appropriate safety and veterinary guidance
- lameness/arthritis: include joint/locomotor tissues when lesions support diagnosis

Dataset impact: syndrome pages and differential matrices should store these sample-selection rules.

### 5. Causality cannot be inferred from pathogen detection alone

The causality chapter supports a key evaluation rule: detecting an organism is not always equivalent to proving it caused the disease. Strong answers should integrate:

- clinical compatibility
- lesion compatibility
- timing and epidemiology
- pathogen load or distribution when relevant
- exclusion of plausible differentials
- response to intervention only as supporting, not standalone, evidence

Dataset impact: judge prompts should penalize answers that treat a positive test or historical exposure as conclusive without matching clinical and pathological evidence.

### 6. Disease control requires host-pathogen-environment thinking

The disease-control chapter is useful for strengthening prevention and biosecurity sections. Control measures should be selected from the problem context:

- host susceptibility and production stage
- pathogen shedding and survival
- environmental pressure
- direct and indirect contact routes
- persistence within herd or between herds
- transportation, feed, people, equipment, and dead-pig movement risks

Dataset impact: management recommendations should not be generic. For high-risk contagious disease, movement restriction, isolation, cleaning/disinfection, and investigation of introduction routes should be expected.

### 7. Biosecurity should cover within-farm and between-farm routes

The first 200 pages strongly support biosecurity boundary checks. Important routes include:

- live animal introduction
- dead pig handling
- transport vehicles and routing
- feed and ingredient delivery
- people, clothing, footwear, and equipment
- shared tools and direct-entry supplies
- untreated food exposure

Dataset impact: high-risk disease answers should include no-sale/no-transport boundaries and practical separation of people, vehicles, tools, and animal movement.

### 8. Drug therapy must start with an objective and a regulatory boundary

The drug therapy chapter supports the current decision not to train specific doses or withdrawal periods without label-level sources. A safe generated answer should distinguish:

- treatment objective
- whether treatment is plausible or mainly supportive
- route feasibility in swine production logistics
- antimicrobial stewardship and resistance risk
- regulatory constraints
- withdrawal and residue responsibility
- outcome monitoring and treatment failure reassessment

Dataset impact: `prescription` should remain directional unless a jurisdiction-specific authoritative drug label is available. The dataset should not include executable dose or fixed withdrawal-period training examples by default.

### 9. Prophylaxis and mass medication require caution

The drug chapter also supports a stricter rule for questions such as "should I treat the whole group?" A good answer should avoid automatic whole-herd antimicrobial use and should prefer:

- diagnosis or strong presumptive evidence
- veterinary oversight
- risk-based group management
- sampling/diagnostics before escalation when possible
- review of outcomes and stopping rules

Dataset impact: answers that recommend broad antimicrobial escalation without testing or veterinary boundary should be review or reject.

### 10. Anesthesia and surgery content has limited dataset relevance

The first 200 pages include anesthesia/surgical material, but this is less central to disease QA generation. It should mainly support boundary rules:

- do not generate surgical/anesthetic protocols unless the task explicitly asks for veterinary procedural support
- do not provide executable sedative/anesthetic dosages in train-ready disease QA
- route, restraint, and monitoring details require professional veterinary context

Dataset impact: most swine disease QA should avoid anesthesia instructions unless explicitly relevant.

## What this source can solve now

This material can immediately improve these current wiki issues:

1. Weak generic sampling language.
2. Lack of diagnostic-process constraints in generated answers.
3. Weak causality and test-interpretation boundaries.
4. Generic biosecurity recommendations.
5. Weak drug-use and withdrawal-period safety rules.
6. Insufficient generation/evaluation rubrics for herd-level case realism.

## What this source cannot solve alone

This material cannot fully solve these current wiki issues:

1. Single-disease clinical signs and lesions for all 73 diseases.
2. Disease-specific laboratory tests for each disease page.
3. Disease-specific differential diagnosis matrices.
4. China-specific regulatory status for each disease.
5. China-specific drug label dosage and withdrawal periods.
6. Detailed antimicrobial selection by pathogen and label.

## Recommended wiki integration

Use this digest in retrieval alongside:

1. target disease page
2. relevant syndrome page
3. differential matrix
4. rule cards
5. drug boundary page when medication appears
6. source pages `SRC-0003`, `SRC-0008`, `SRC-0009`, `SRC-0010`, `SRC-0011`, `SRC-0012`, and `SRC-0013`

## Generation checklist additions

Generated swine disease QA should include:

- a realistic farm-level question with stage, group size, spread, duration, and management context
- a diagnosis that explains evidence and uncertainty
- at least one syndrome-appropriate sample/testing suggestion when signs are nonspecific or high risk
- a control plan that addresses movement, isolation, and environmental or biosecurity routes
- a drug-use boundary that avoids specific dosage and fixed withdrawal-period numbers unless a label source is present

## Evaluation checklist additions

Judge and arbiter prompts should check:

- whether the answer considered herd-level context
- whether diagnosis is overclaimed from insufficient evidence
- whether sampling is syndrome-appropriate
- whether pathogen detection is interpreted with clinical/lesion context
- whether biosecurity routes match the disease risk
- whether drug advice is objective-driven and regulatory-safe
- whether any specific dosage or fixed withdrawal period appears without authoritative label support

## Issue audit linkage

This digest partially addresses the issue categories:

- "实验室诊断与采样建议不足"
- "防控、上报、禁售、禁运边界不足"
- "药物页与食品安全边界不足"
- "数据生成流程仍存在的问题"
- "评估流程仍存在的问题"

It does not replace the need to upgrade individual disease pages.
