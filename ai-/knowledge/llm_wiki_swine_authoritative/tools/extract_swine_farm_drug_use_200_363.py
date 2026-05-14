import extract_swine_farm_drug_use_1_200 as base


base.RAW = base.ROOT / "raw" / "md" / "猪场兽药使用与猪病防治技术200-363页.md"
base.SOURCE_ID = "SRC-0090"
base.BOOK_TITLE = "猪场兽药使用与猪病防治技术（200-363页）"
base.CONTINUATION_MODE = True

base.OUT_JSON = base.ROOT / "issues" / "swine_farm_drug_use_200_363_facts_v13_1.json"
base.OUT_FACT_CSV = base.ROOT / "exports" / "swine_farm_drug_use_200_363_fact_index.csv"
base.OUT_DRUG_CSV = base.ROOT / "exports" / "swine_farm_drug_use_200_363_drug_mention_index.csv"
base.OUT_MD = base.ROOT / "wiki" / "synthesis" / "swine_farm_drug_use_200_363_treatment_matrix.md"
base.REPORT = base.ROOT / "issues" / "swine_farm_drug_use_200_363_batch_progress_2026-05-08.md"
base.SOURCE_PAGE = base.ROOT / "wiki" / "sources" / "SRC-0090-swine-farm-drug-use-and-disease-control-200-363.md"

base.START = "<!-- SFDUT_200_363_V13_1_START -->"
base.END = "<!-- SFDUT_200_363_V13_1_END -->"


if __name__ == "__main__":
    base.main()
