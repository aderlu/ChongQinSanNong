---
type: synthesis
page_id: swine_textbook_pages_201_400_system_digest
title: Diseases of Swine 11e pages 201-400 system digest
category: system_pathology_differential
derived: true
updated: 2026-05-08T23:59:00+08:00
source_trust: authoritative
evidence_coverage: complete
usage_scope: [retrieval, audit_only, source_digest]
sources:
  - SRC-0013
  - SRC-0014
  - SRC-0015
  - SRC-0016
  - SRC-0017
  - SRC-0018
  - SRC-0019
  - SRC-0020
  - SRC-0021
  - SRC-0022
  - SRC-0023
  - SRC-0024
raw_source: raw/md/201-400.md
---

# Diseases of Swine 11e pages 201-400 system digest

This page summarizes operational knowledge extracted from `raw/md/201-400.md`, the markdown extraction of *Diseases of Swine, 11th Edition* pages 201-400. It is a derived synthesis page for retrieval, generation, and evaluation. It does not replace the underlying source pages, Chinese official regulatory sources, product labels, or veterinary case judgment.

## Coverage assessment

Pages 201-400 are not primarily single-disease chapters. They contain the end of anesthesia and surgery material, then several high-value system and public-health chapters:

- anesthesia, analgesia, surgery, castration, prolapse, hernia, gastric ulcer, arthritis, and surgical complication boundaries
- preharvest food safety, zoonotic disease, antimicrobial resistance, residues, show-pig drug testing, and human-health interface
- show and pet pig biosecurity, movement, stress, individual-animal medicine, and ethical boundaries
- cardiovascular and hematopoietic system pathology, including anemia, shock, heart failure, pericarditis, myocarditis, mulberry heart disease, thrombosis, edema, and neoplasia
- digestive system physiology, diarrhea mechanisms, gut lesion patterns, common gastrointestinal differential tables, diagnostic confirmation, peritoneal/liver/pancreas pathology, and enteric disease red flags
- immune system, neonatal passive immunity, mucosal immunity, immune dysfunction, maternal antibody interference, herd immunity, vaccination failure, autogenous vaccine, and planned exposure boundaries
- integumentary system, skin history, lesion classification, biopsy/scraping/culture/PCR, bacterial/viral/fungal/parasitic/environmental/nutritional skin differentials, hoof and claw lesions
- mammary system, colostrum, milk production, passive immunity, mastitis, and postpartum dysgalactia syndrome (PDS)
- nervous and locomotor system opening, neurological/locomotor examination, antemortem and postmortem sampling, congenital neurologic and locomotor differentials, toxic/nutritional/infectious neurologic boundaries, lameness and arthritis
- reproductive system opening, herd-level reproductive diagnostic approach, individual pig examination, puberty and early fertility problem framing

This material can solve several system-level knowledge gaps, especially where the wiki lacks clinically useful syndrome pages, differential matrices, lesion patterns, and evaluation rules. It still cannot fully solve disease-specific pages for every pathogen or jurisdiction-specific regulatory rules.

## Knowledge absorbed from pages 201-400

### 1. Surgical and procedural material should become safety boundaries, not train-ready protocols

The anesthesia and surgery continuation contains detailed procedural content. For swine disease QA generation, the useful integration is boundary-oriented:

- do not generate executable anesthesia, epidural, surgical, castration, prolapse, hernia, or amputation protocols in general disease QA
- do recognize procedure-related complications as disease-like differentials, such as post-castration hemorrhage, abscess, scirrhous cord, inguinal hernia, urinary obstruction, prolapse, septic arthritis, seroma, hematoma, and welfare compromise
- when a case involves surgery, emphasize veterinary examination, pain control, monitoring, asepsis, residue/legal review, and complication triage rather than fixed doses or step-by-step procedures
- food-chain animals require residue and withdrawal-boundary attention whenever perioperative antimicrobials, anti-inflammatory drugs, sedatives, or hormones are mentioned

Dataset impact: reject or review outputs that turn this chapter into procedural instructions or fixed drug protocols. Use it mainly to enrich differential diagnosis and safety review.

### 2. Preharvest food safety connects farm medicine to human-health risk

The food-safety chapter directly helps current wiki gaps in drug, food-safety, and public-health boundaries.

Use in generation and evaluation:

- answers involving market pigs should consider physical hazards such as broken needles when injections are described
- chemical hazards include extra-label drug use, residues, feed contaminants, environmental contaminants, and dioxin-like risks; local law and label sources are required before making compliance claims
- biological hazards include foodborne organisms associated with pork and swine environments, including Salmonella, Campylobacter, Yersinia enterocolitica, Shiga toxin-producing E. coli, Trichinella, Toxoplasma, and Taenia solium
- non-foodborne zoonotic risks include MRSA, Streptococcus suis, Clostridium difficile, influenza A viruses, hepatitis E virus, Japanese encephalitis virus, Nipah virus, and Reston ebolavirus
- antimicrobial resistance is a public-health boundary, not only a treatment-efficacy issue

Dataset impact: answers about treatment, slaughter, sale, show pigs, human exposure, or pork safety should include a food-safety boundary when relevant. The textbook can support hazard awareness, but Chinese MRLs, withdrawal times, testing rules, and official disposal/recall decisions still require A0/A1 sources.

### 3. Show and pet pigs need a separate scenario model

Show pigs and miniature pet pigs differ from commercial-herd cases.

Use in generation and evaluation:

- show pigs have high movement, commingling, exhibition, transport, stress, and human-contact exposure, so biosecurity and zoonotic education should be explicit
- drug-use answers for show pigs must consider testing, ethics, label/legal status, food-chain status, and event rules; do not promise that an animal will pass a test
- individual-animal medicine is more common in show and pet pigs, but sedation, restraint, surgery, and medication still require professional boundaries
- pet pigs may still intersect with food-animal drug rules depending on jurisdiction and status; the wiki should not assume pet status removes all residue/legal constraints

Dataset impact: user queries about fairs, exhibitions, sale barns, club pigs, school pigs, pet pigs, or miniature pigs should retrieve this digest and relevant biosecurity/drug-boundary pages.

### 4. Cardiovascular and hematopoietic content improves acute death and anemia differentials

The cardiovascular chapter is valuable for syndrome-level pages rather than single infectious disease pages.

Use in differential diagnosis:

- sudden death, cyanosis, pallor, edema, ascites, shock, poor growth, and exercise intolerance need cardiovascular and hematopoietic differential framing
- mulberry heart disease is a noninfectious acute cardiac condition that can resemble sudden-death infectious problems
- pericarditis, myocarditis, endocarditis, thrombosis, vascular inflammation, and heart failure can arise from systemic infections or noninfectious causes
- anemia should be differentiated by defective erythropoiesis, hemolysis, hemorrhage, and hemoglobin disorders rather than treated as one disease
- body-cavity fluid and edema should be interpreted with heart, liver, kidney, protein, anemia, and inflammatory context

Dataset impact: acute-death and pallor/anemia cases should not be forced into ASF/CSF/septicemia without lesion and herd-context support. The answer should mention appropriate necropsy and laboratory confirmation when the presentation is nonspecific.

### 5. Digestive system chapter is a major answer to the current diarrhea differential gap

The digestive system chapter is the strongest part of pages 201-400 for immediate wiki improvement. It supplies mechanisms, age windows, lesion patterns, and diagnostic confirmation for common enteric conditions.

Core diarrhea mechanisms:

- hypersecretion
- malabsorption
- inflammation
- increased intestinal permeability
- hemorrhage or ulceration
- obstruction, torsion, or vascular compromise

Important differential signals:

- ETEC/EPEC: neonatal or post-weaning watery diarrhea, dehydration, and virulence testing context
- rotavirus: suckling to young pigs, watery to pasty diarrhea, villous atrophy, PCR/ELISA/PAGE or tissue visualization
- Clostridium perfringens type C: neonatal hemorrhagic/necrotic enteritis and sudden death, confirmed with compatible lesions and toxin/testing context
- Clostridium difficile: suckling-pig creamy diarrhea, mesocolonic edema, toxin and histopathology context
- Cystoisospora suis: suckling-pig yellow diarrhea, villous atrophy, fibrinonecrotic enteritis, impression smear/fecal float/histopath context
- TGE/PED/PDCoV: all-age watery diarrhea, vomiting, rapid dehydration and mortality in susceptible piglets, severe villous atrophy, PCR plus lesion/visualization context
- PCV2: diarrhea with wasting and multisystemic disease; qPCR alone is suggestive, not definitive without lesions and tissue localization
- Lawsonia: ileal/intestinal proliferation, proliferative hemorrhagic enteropathy, fresh blood clots, PCR/serology plus lesion confirmation
- Brachyspira: large-intestinal mucohemorrhagic colitis; culture/PCR and histologic localization support diagnosis
- Salmonella: post-weaning or all-age enteric/septicemic patterns, fibrinous or hemorrhagic colitis, focal ulcers, liver nodules, culture/PCR/serotype context
- Trichuris and Oesophagostomum: weaning-to-adult colitis, sometimes mucohemorrhagic, easily missed when antibiotics fail
- gastric ulceration: melena, pallor, anemia, sudden death after weaning, pars esophagea lesions
- torsion/hemorrhagic bowel syndrome: sudden death with distended dark intestine, often before fecal blood is seen

Diagnostic boundary:

- detection of endemic enteric agents by culture, PCR, or metagenomics is not sufficient to establish causation without a defined history, clinical presentation, and compatible gross or microscopic lesions
- histopathology is critical in mixed infections and in nonspecific colitis or dysbacteriosis
- serious epidemic diseases such as CSF and ASF can have enteric components and must trigger reporting/investigation boundaries rather than routine diarrhea treatment

Dataset impact: this chapter can directly improve piglet diarrhea, post-weaning diarrhea, hemorrhagic diarrhea, melena, sudden-death-enteric, and poor-growth syndromes. It supports both syndrome pages and differential matrices.

### 6. Immune-system content improves vaccine, colostrum, and co-infection reasoning

The immune chapter helps prevent simplistic "vaccinate or medicate" answers.

Use in generation and evaluation:

- newborn piglets rely on colostrum and passive immunity; inadequate colostrum intake is a major neonatal risk factor
- mucosal immunity, maternal antibody, production stage, nutrition, stress, and coinfections shape disease expression
- infectious agents can induce immune dysfunction and increase susceptibility to secondary infections or immunopathology
- PRRSV, PCV2, influenza, Mycoplasma hyopneumoniae, Actinobacillus pleuropneumoniae, PRV, Salmonella, and other agents can interact with immune response and respiratory/enteric disease severity
- herd immunity and interval/route issues matter when evaluating vaccination programs
- vaccination failure can reflect timing, maternal antibody interference, handling, antigen mismatch, storage, administration route, herd pressure, immunosuppression, or unrealistic expectations
- autogenous vaccines and planned exposure require strict professional, biosecurity, regulatory, and welfare boundaries

Dataset impact: vaccine and prevention answers should avoid fixed programs unless supported by product/regulatory sources. For "vaccine did not work" cases, the answer should explore timing, storage, route, maternal antibodies, challenge pressure, and coinfections.

### 7. Skin, hoof, and claw chapter improves lesion-based triage

The integumentary chapter supplies a practical structure for skin cases.

Use in generation and evaluation:

- skin cases should include age, distribution, environment, season, nutrition, group spread, pruritus, pain, crusts, vesicles, erosions, ulcers, necrosis, and hoof/claw involvement
- lesion description should distinguish primary lesions from secondary changes caused by trauma, scratching, infection, or management
- sampling should be lesion-appropriate: skin biopsy, direct examination/scraping, culture, and PCR may be needed depending on the syndrome
- greasy pig disease, pustular dermatitis, ear necrosis, ulcerative dermatitis, facial necrosis, erysipelas skin lesions, swinepox, vesicular diseases, dermatophytosis, mange/lice, sunburn, photosensitization, frostbite, parakeratosis, congenital conditions, and hoof/claw lesions belong in the skin differential space
- vesicular or hemorrhagic/necrotic skin presentations can overlap with reportable diseases and should trigger regulatory review boundaries

Dataset impact: skin cases should not be answered only with "use antibiotics and disinfect." They need lesion distribution, sampling, differential diagnosis, and food-safety/drug boundaries.

### 8. Mammary system chapter improves lactation, colostrum, and PDS pages

The mammary chapter is highly relevant to neonatal piglet survival and sow post-farrowing disorders.

Use in generation and evaluation:

- poor colostrum intake and uneven teat access can drive neonatal weakness, poor passive immunity, and later disease susceptibility
- cross-fostering and split suckling are management concepts, but should be presented as veterinary/herd-management guidance rather than fixed universal instructions
- mammary gland use affects milk yield in the current and later lactations
- PDS and mastitis require evaluation of sow signs, udder findings, piglet behavior, farrowing context, environment, nutrition, water, and management
- therapy for diseased sows must remain directional without fixed drug/dose/withdrawal statements unless label-level sources exist

Dataset impact: neonatal diarrhea or weak-piglet cases should consider colostrum and lactation context. PDS cases should not be collapsed into a single infectious diagnosis without management and sow/piglet evidence.

### 9. Nervous and locomotor content improves neurologic and lameness sampling

The nervous and locomotor chapter opening supports existing syndrome pages.

Use in generation and evaluation:

- neurologic cases need lesion localization thinking: forebrain/cerebral cortex, cerebellum, spinal cord, vestibular/eyes, peripheral nerve, muscle, bone, or joint
- antemortem sampling and postmortem sampling should be selected according to clinical localization and safety
- congenital tremor, splayleg, hypoxia, hypoglycemia, hydrocephalus, cerebellar hypoplasia, vitamin A-related issues, viral pathogens, bacterial agents, toxins, deficiencies, salt poisoning/water deprivation, gases, and plant/insecticide poisonings belong in neurologic differentials
- lameness should distinguish bone, joint, muscle, hoof/claw, fracture, osteochondrosis, infectious arthritis, polyarthritis, nutritional myopathy, and sow/boar locomotor disorders
- joint or locomotor infection should not be assumed from lameness alone; lesion distribution and sampling matter

Dataset impact: neurologic QA should include safety/reporting boundaries when rabies, JEV, pseudorabies, salt poisoning, water deprivation, toxins, or high-mortality systemic disease are plausible.

### 10. Reproductive-system opening improves herd-level reproductive questions

The reproductive chapter begins near the end of `201-400.md`, so this digest only uses it as an opening anchor.

Use in generation and evaluation:

- reproductive problems should be framed at herd level before choosing one pathogen
- records, parity distribution, puberty attainment, weaning-to-estrus interval, conception/farrowing rates, returns, abortion timing, stillbirths, mummification, and individual sow/gilt examination matter
- ultrasonography and individual examination can support herd investigations, but fixed reproductive-drug or hormone protocols should not be generated
- infectious causes such as PRRSV, PPV, leptospirosis, pseudorabies, brucellosis, and JEV require disease-specific chapters and regulatory sources for final boundaries

Dataset impact: reproductive failure cases should retrieve this digest plus the reproductive-failure syndrome page and disease-specific pages.

## What this source can solve now

Pages 201-400 can materially improve these wiki gaps:

1. Syndrome-level differential diagnosis for diarrhea, hemorrhagic diarrhea, melena, acute death, anemia, skin lesions, lameness, neurologic signs, weak piglets, PDS, and reproductive failure opening.
2. Lesion-pattern and gross/histology/test matching for enteric diseases.
3. Food-safety, zoonosis, and AMR boundaries for treatment, slaughter, human exposure, show pigs, and pork safety.
4. Vaccine and immunity evaluation boundaries, including colostrum, maternal antibody, herd immunity, and vaccination failure.
5. Skin and hoof diagnostic sampling boundaries.
6. Nervous/locomotor diagnostic localization and sampling boundaries.
7. Procedure-related complications as differentials while avoiding unsafe procedural generation.

## What this source cannot solve alone

Pages 201-400 still cannot fully solve:

1. Disease-specific single-pathogen pages for all 73 diseases.
2. China-specific regulatory status, reporting, quarantine, no-sale/no-transport, disposal, or residue enforcement.
3. China-specific drug labels, dosage, treatment duration, withdrawal periods, MRLs, or testing decisions.
4. Complete reproductive-system details because the chapter continues beyond page 400.
5. Respiratory and urinary system content, which appears in later page segments.
6. Full differential matrices with source-linked rows for every high-risk disease pair.

## Recommended wiki integration

Use this digest in retrieval alongside:

1. target disease page
2. relevant syndrome page
3. `swine_textbook_pages_1_200_crosscutting_digest.md`
4. `swine_differential_diagnosis_matrix.md`
5. `swine_sampling_and_lab_diagnosis_boundary.md`
6. `swine_public_health_food_safety_boundary.md`
7. `swine_drug_and_withdrawal_boundary.md`
8. relevant source pages `SRC-0013` through `SRC-0024`

## Generation checklist additions

Generated swine QA should include:

- production stage and syndrome pattern when asking about diarrhea, skin disease, lameness, neurologic signs, acute death, weak piglets, PDS, or reproductive failure
- lesion and sample suggestions matched to the body system
- food-safety and human-exposure boundaries when market animals, show pigs, zoonoses, drug residues, or pork safety are relevant
- differential diagnosis for common enteric syndromes using age, lesion, and test context
- vaccine/immunity reasoning when the question involves colostrum, maternal antibodies, herd immunity, vaccine failure, or coinfection
- no executable surgery/anesthesia protocols or fixed drug/dose/withdrawal statements without explicit authority

## Evaluation checklist additions

Judge and arbiter prompts should check:

- whether diarrhea answers distinguish age, mechanism, lesion, and diagnostic confirmation
- whether positive PCR/culture for endemic enteric agents is overinterpreted without compatible lesions and history
- whether skin answers describe lesion type, distribution, sampling, and reportable-disease boundaries when needed
- whether neurologic and lameness answers localize the problem before naming a disease
- whether weak-piglet and neonatal disease answers consider colostrum/lactation context
- whether treatment or show-pig answers mention food-safety, residues, testing, and legal boundaries
- whether any surgical or anesthetic content becomes unsafe procedural instruction
