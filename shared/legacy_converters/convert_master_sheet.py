# ********************
# imports python
# ********************
import traceback

# ********************
# imports django
# ********************
# ********************
# imports shared
# ********************
from shared.utils import utils_logger
from shared.legacy_converters import converter_utils

# ********************
# imports app
# ********************
from apps.main import models as main_models

# *************************************************************************
# API ROUTE
# *************************************************************************

PERIOD_NATIONAL = {"start": 1964, "end": 1990}
PERIOD_STATES = {"start": 1990, "end": 2019}

response_model = [
    {"name": "Period", "indicator": "", "datasource": ""},
    {"name": "State", "indicator": "", "datasource": ""},
    {
        "name": "ANC Coverage (4 visits) -> MICS",
        "indicator": "ANC Coverage (4 visits)",
        "datasource": "MICS",
    },
    {
        "name": "ANC Coverage (4 visits) -> NARHS",
        "indicator": "ANC Coverage (4 visits)",
        "datasource": "NARHS",
    },
    {
        "name": "ANC Coverage (4 visits) -> NDHS",
        "indicator": "ANC Coverage (4 visits)",
        "datasource": "NDHS",
    },
    {
        "name": "ANC Coverage (4 visits) -> NHMIS",
        "indicator": "ANC Coverage (4 visits)",
        "datasource": "NHMIS",
    },
    {
        "name": "ANC Coverage (4 visits) -> NNHS",
        "indicator": "ANC Coverage (4 visits)",
        "datasource": "NNHS",
    },
    {
        "name": "ANC Coverage (4 visits) -> WHO-GHO",
        "indicator": "ANC Coverage (4 visits)",
        "datasource": "WHO-GHO",
    },
    {
        "name": "ANC Coverage (4 visits) -> World Bank",
        "indicator": "ANC Coverage (4 visits)",
        "datasource": "World Bank",
    },
    {
        "name": "ANC Coverage (at least 1 visit) -> KDGHS",
        "indicator": "ANC Coverage (at least 1 visit)",
        "datasource": "KDGHS",
    },
    {
        "name": "ANC Coverage (at least 1 visit) -> MICS",
        "indicator": "ANC Coverage (at least 1 visit)",
        "datasource": "MICS",
    },
    {
        "name": "ANC Coverage (at least 1 visit) -> NARHS",
        "indicator": "ANC Coverage (at least 1 visit)",
        "datasource": "NARHS",
    },
    {
        "name": "ANC Coverage (at least 1 visit) -> NDHS",
        "indicator": "ANC Coverage (at least 1 visit)",
        "datasource": "NDHS",
    },
    {
        "name": "ANC Coverage (at least 1 visit) -> NHMIS",
        "indicator": "ANC Coverage (at least 1 visit)",
        "datasource": "NHMIS",
    },
    {
        "name": "ANC Coverage (at least 1 visit) -> NMIS",
        "indicator": "ANC Coverage (at least 1 visit)",
        "datasource": "NMIS",
    },
    {
        "name": "ANC Coverage (at least 1 visit) -> NNHS",
        "indicator": "ANC Coverage (at least 1 visit)",
        "datasource": "NNHS",
    },
    {
        "name": "Adolescent birth rate -> IHME",
        "indicator": "Adolescent birth rate",
        "datasource": "IHME",
    },
    {
        "name": "Adolescent birth rate -> MICS",
        "indicator": "Adolescent birth rate",
        "datasource": "MICS",
    },
    {
        "name": "Adolescent birth rate -> NDHS",
        "indicator": "Adolescent birth rate",
        "datasource": "NDHS",
    },
    {
        "name": "Adolescent birth rate -> NMIS",
        "indicator": "Adolescent birth rate",
        "datasource": "NMIS",
    },
    {
        "name": "Adolescent birth rate -> WHO-GHO",
        "indicator": "Adolescent birth rate",
        "datasource": "WHO-GHO",
    },
    {
        "name": "Adolescent birth rate -> World Bank",
        "indicator": "Adolescent birth rate",
        "datasource": "World Bank",
    },
    {
        "name": "Contraceptive prevalence rate -> IHME",
        "indicator": "Contraceptive prevalence rate",
        "datasource": "IHME",
    },
    {
        "name": "Contraceptive prevalence rate -> MICS",
        "indicator": "Contraceptive prevalence rate",
        "datasource": "MICS",
    },
    {
        "name": "Contraceptive prevalence rate -> NARHS",
        "indicator": "Contraceptive prevalence rate",
        "datasource": "NARHS",
    },
    {
        "name": "Contraceptive prevalence rate -> NDHS",
        "indicator": "Contraceptive prevalence rate",
        "datasource": "NDHS",
    },
    {
        "name": "Contraceptive prevalence rate -> NHMIS",
        "indicator": "Contraceptive prevalence rate",
        "datasource": "NHMIS",
    },
    {
        "name": "Contraceptive prevalence rate -> NNHS",
        "indicator": "Contraceptive prevalence rate",
        "datasource": "NNHS",
    },
    {
        "name": "Contraceptive prevalence rate -> WHO-GHO",
        "indicator": "Contraceptive prevalence rate",
        "datasource": "WHO-GHO",
    },
    {
        "name": "Contraceptive prevalence rate -> World Bank",
        "indicator": "Contraceptive prevalence rate",
        "datasource": "World Bank",
    },
    {
        "name": "DPT 3/Penta 3 coverage rate -> IHME",
        "indicator": "DPT 3/Penta 3 coverage rate",
        "datasource": "IHME",
    },
    {
        "name": "DPT 3/Penta 3 coverage rate -> KDGHS",
        "indicator": "DPT 3/Penta 3 coverage rate",
        "datasource": "KDGHS",
    },
    {
        "name": "DPT 3/Penta 3 coverage rate -> MICS",
        "indicator": "DPT 3/Penta 3 coverage rate",
        "datasource": "MICS",
    },
    {
        "name": "DPT 3/Penta 3 coverage rate -> NDHS",
        "indicator": "DPT 3/Penta 3 coverage rate",
        "datasource": "NDHS",
    },
    {
        "name": "DPT 3/Penta 3 coverage rate -> NHMIS",
        "indicator": "DPT 3/Penta 3 coverage rate",
        "datasource": "NHMIS",
    },
    {
        "name": "DPT 3/Penta 3 coverage rate -> NNHS",
        "indicator": "DPT 3/Penta 3 coverage rate",
        "datasource": "NNHS",
    },
    {
        "name": "DPT 3/Penta 3 coverage rate -> WHO-GHO",
        "indicator": "DPT 3/Penta 3 coverage rate",
        "datasource": "WHO-GHO",
    },
    {
        "name": "DPT 3/Penta 3 coverage rate -> World Bank",
        "indicator": "DPT 3/Penta 3 coverage rate",
        "datasource": "World Bank",
    },
    {"name": "IPV coverage rate -> IHME", "indicator": "IPV coverage rate", "datasource": "IHME"},
    {"name": "IPV coverage rate -> MICS", "indicator": "IPV coverage rate", "datasource": "MICS"},
    {"name": "IPV coverage rate -> NHMIS", "indicator": "IPV coverage rate", "datasource": "NHMIS"},
    {
        "name": "Infant Mortality rate -> MICS",
        "indicator": "Infant Mortality rate",
        "datasource": "MICS",
    },
    {
        "name": "Infant Mortality rate -> NARHS",
        "indicator": "Infant Mortality rate",
        "datasource": "NARHS",
    },
    {
        "name": "Infant Mortality rate -> NDHS",
        "indicator": "Infant Mortality rate",
        "datasource": "NDHS",
    },
    {
        "name": "Infant Mortality rate -> NHMIS",
        "indicator": "Infant Mortality rate",
        "datasource": "NHMIS",
    },
    {
        "name": "Infant Mortality rate -> NMIS",
        "indicator": "Infant Mortality rate",
        "datasource": "NMIS",
    },
    {
        "name": "Infant Mortality rate -> WHO-GHO",
        "indicator": "Infant Mortality rate",
        "datasource": "WHO-GHO",
    },
    {
        "name": "Infant Mortality rate -> World Bank",
        "indicator": "Infant Mortality rate",
        "datasource": "World Bank",
    },
    {
        "name": "Maternal Mortality Ratio -> IHME",
        "indicator": "Maternal Mortality Ratio",
        "datasource": "IHME",
    },
    {
        "name": "Maternal Mortality Ratio -> NARHS",
        "indicator": "Maternal Mortality Ratio",
        "datasource": "NARHS",
    },
    {
        "name": "Maternal Mortality Ratio -> NDHS",
        "indicator": "Maternal Mortality Ratio",
        "datasource": "NDHS",
    },
    {
        "name": "Maternal Mortality Ratio -> NHMIS",
        "indicator": "Maternal Mortality Ratio",
        "datasource": "NHMIS",
    },
    {
        "name": "Maternal Mortality Ratio -> WHO-GHO",
        "indicator": "Maternal Mortality Ratio",
        "datasource": "WHO-GHO",
    },
    {
        "name": "Maternal Mortality Ratio -> World Bank",
        "indicator": "Maternal Mortality Ratio",
        "datasource": "World Bank",
    },
    {
        "name": "Measles Immunization Coverage -> IHME",
        "indicator": "Measles Immunization Coverage",
        "datasource": "IHME",
    },
    {
        "name": "Measles Immunization Coverage -> KDGHS",
        "indicator": "Measles Immunization Coverage",
        "datasource": "KDGHS",
    },
    {
        "name": "Measles Immunization Coverage -> MICS",
        "indicator": "Measles Immunization Coverage",
        "datasource": "MICS",
    },
    {
        "name": "Measles Immunization Coverage -> NDHS",
        "indicator": "Measles Immunization Coverage",
        "datasource": "NDHS",
    },
    {
        "name": "Measles Immunization Coverage -> NHMIS",
        "indicator": "Measles Immunization Coverage",
        "datasource": "NHMIS",
    },
    {
        "name": "Measles Immunization Coverage -> NNHS",
        "indicator": "Measles Immunization Coverage",
        "datasource": "NNHS",
    },
    {
        "name": "Measles Immunization Coverage -> PCCS",
        "indicator": "Measles Immunization Coverage",
        "datasource": "",
    },
    {
        "name": "Measles Immunization Coverage -> WHO-GHO",
        "indicator": "Measles Immunization Coverage",
        "datasource": "WHO-GHO",
    },
    {
        "name": "Measles Immunization Coverage -> World Bank",
        "indicator": "Measles Immunization Coverage",
        "datasource": "World Bank",
    },
    {
        "name": "Neonatal mortality rate (per 1000 live births) -> IHME",
        "indicator": "Neonatal mortality rate (per 1000 live births)",
        "datasource": "IHME",
    },
    {
        "name": "Neonatal mortality rate (per 1000 live births) -> MICS",
        "indicator": "Neonatal mortality rate (per 1000 live births)",
        "datasource": "MICS",
    },
    {
        "name": "Neonatal mortality rate (per 1000 live births) -> NDHS",
        "indicator": "Neonatal mortality rate (per 1000 live births)",
        "datasource": "NDHS",
    },
    {
        "name": "Neonatal mortality rate (per 1000 live births) -> NHMIS",
        "indicator": "Neonatal mortality rate (per 1000 live births)",
        "datasource": "NHMIS",
    },
    {
        "name": "Neonatal mortality rate (per 1000 live births) -> NMIS",
        "indicator": "Neonatal mortality rate (per 1000 live births)",
        "datasource": "NMIS",
    },
    {
        "name": "Neonatal mortality rate (per 1000 live births) -> WHO-GHO",
        "indicator": "Neonatal mortality rate (per 1000 live births)",
        "datasource": "WHO-GHO",
    },
    {
        "name": "Neonatal mortality rate (per 1000 live births) -> World Bank",
        "indicator": "Neonatal mortality rate (per 1000 live births)",
        "datasource": "World Bank",
    },
    {
        "name": "Percentage of children fully immunized against childhood diseases by age 1 -> MICS",
        "indicator": "Percentage of children fully immunized against childhood diseases by age 1",
        "datasource": "MICS",
    },
    {
        "name": "Percentage of children fully immunized against childhood diseases by age 1 -> NDHS",
        "indicator": "Percentage of children fully immunized against childhood diseases by age 1",
        "datasource": "NDHS",
    },
    {
        "name": "Percentage of children fully immunized against childhood diseases by age 1 -> NHMIS",
        "indicator": "Percentage of children fully immunized against childhood diseases by age 1",
        "datasource": "NHMIS",
    },
    {
        "name": "Percentage of children under 5 with fever who received ACT -> MICS",
        "indicator": "Percentage of children under 5 with fever who received ACT",
        "datasource": "MICS",
    },
    {
        "name": "Percentage of children under 5 with fever who received ACT -> NDHS",
        "indicator": "Percentage of children under 5 with fever who received ACT",
        "datasource": "NDHS",
    },
    {
        "name": "Percentage of children under 5 with fever who received ACT -> NMIS",
        "indicator": "Percentage of children under 5 with fever who received ACT",
        "datasource": "NMIS",
    },
    {
        "name": "Percentage of children under 5 with fever who received ACT -> NNHS",
        "indicator": "Percentage of children under 5 with fever who received ACT",
        "datasource": "NNHS",
    },
    {
        "name": "Percentage of children under 6 months who were exclusively breastfed -> IHME",
        "indicator": "Percentage of children under 6 months who were exclusively breastfed",
        "datasource": "IHME",
    },
    {
        "name": "Percentage of children under 6 months who were exclusively breastfed -> MICS",
        "indicator": "Percentage of children under 6 months who were exclusively breastfed",
        "datasource": "MICS",
    },
    {
        "name": "Percentage of children under 6 months who were exclusively breastfed -> NDHS",
        "indicator": "Percentage of children under 6 months who were exclusively breastfed",
        "datasource": "NDHS",
    },
    {
        "name": "Percentage of children under 6 months who were exclusively breastfed -> NNHS",
        "indicator": "Percentage of children under 6 months who were exclusively breastfed",
        "datasource": "NNHS",
    },
    {
        "name": "Percentage of children under 6 months who were exclusively breastfed -> WHO-GHO",
        "indicator": "Percentage of children under 6 months who were exclusively breastfed",
        "datasource": "WHO-GHO",
    },
    {
        "name": "Percentage of children under 6 months who were exclusively breastfed -> World Bank",
        "indicator": "Percentage of children under 6 months who were exclusively breastfed",
        "datasource": "World Bank",
    },
    {
        "name": "Percentage of children with diarrhoea who received treatment -> KDGHS",
        "indicator": "Percentage of children with diarrhoea who received treatment",
        "datasource": "KDGHS",
    },
    {
        "name": "Percentage of children with diarrhoea who received treatment -> MICS",
        "indicator": "Percentage of children with diarrhoea who received treatment",
        "datasource": "MICS",
    },
    {
        "name": "Percentage of children with diarrhoea who received treatment -> NDHS",
        "indicator": "Percentage of children with diarrhoea who received treatment",
        "datasource": "NDHS",
    },
    {
        "name": "Percentage of children with diarrhoea who received treatment -> NNHS",
        "indicator": "Percentage of children with diarrhoea who received treatment",
        "datasource": "NNHS",
    },
    {
        "name": "Percentage of children with diarrhoea who received treatment -> WHO-GHO",
        "indicator": "Percentage of children with diarrhoea who received treatment",
        "datasource": "WHO-GHO",
    },
    {
        "name": "Percentage of children with diarrhoea who received treatment -> World Bank",
        "indicator": "Percentage of children with diarrhoea who received treatment",
        "datasource": "World Bank",
    },
    {
        "name": "Percentage of people age 15-49 years who have been tested for HIV and know their results -> MICS",
        "indicator": "Percentage of people age 15-49 years who have been tested for HIV and know their results",
        "datasource": "MICS",
    },
    {
        "name": "Percentage of people age 15-49 years who have been tested for HIV and know their results -> NARHS",
        "indicator": "Percentage of people age 15-49 years who have been tested for HIV and know their results",
        "datasource": "NARHS",
    },
    {
        "name": "Percentage of people age 15-49 years who have been tested for HIV and know their results -> NDHS",
        "indicator": "Percentage of people age 15-49 years who have been tested for HIV and know their results",
        "datasource": "NDHS",
    },
    {
        "name": "Percentage of pregnant women tested for HIV during antenatal care -> MICS",
        "indicator": "Percentage of pregnant women tested for HIV during antenatal care",
        "datasource": "MICS",
    },
    {
        "name": "Percentage of pregnant women tested for HIV during antenatal care -> NARHS",
        "indicator": "Percentage of pregnant women tested for HIV during antenatal care",
        "datasource": "NARHS",
    },
    {
        "name": "Percentage of pregnant women tested for HIV during antenatal care -> NDHS",
        "indicator": "Percentage of pregnant women tested for HIV during antenatal care",
        "datasource": "NDHS",
    },
    {
        "name": "Percentage of pregnant women tested for HIV during antenatal care -> NNHS",
        "indicator": "Percentage of pregnant women tested for HIV during antenatal care",
        "datasource": "NNHS",
    },
    {
        "name": "Percentage of pregnant women tested for HIV during antenatal care -> UNAIDS",
        "indicator": "Percentage of pregnant women tested for HIV during antenatal care",
        "datasource": "UNAIDS",
    },
    {
        "name": "Percentage of women age 15-49 years who received at least one IPT dose during pregnancy -> MICS",
        "indicator": "Percentage of women age 15-49 years who received at least one IPT dose during pregnancy",
        "datasource": "MICS",
    },
    {
        "name": "Percentage of women age 15-49 years who received at least one IPT dose during pregnancy -> NARHS",
        "indicator": "Percentage of women age 15-49 years who received at least one IPT dose during pregnancy",
        "datasource": "NARHS",
    },
    {
        "name": "Percentage of women age 15-49 years who received at least one IPT dose during pregnancy -> NDHS",
        "indicator": "Percentage of women age 15-49 years who received at least one IPT dose during pregnancy",
        "datasource": "NDHS",
    },
    {
        "name": "Percentage of women age 15-49 years who received at least one IPT dose during pregnancy -> NMIS",
        "indicator": "Percentage of women age 15-49 years who received at least one IPT dose during pregnancy",
        "datasource": "NMIS",
    },
    {
        "name": "Percentage of women age 15-49 years who received at least one IPT dose during pregnancy -> NNHS",
        "indicator": "Percentage of women age 15-49 years who received at least one IPT dose during pregnancy",
        "datasource": "NNHS",
    },
    {
        "name": "Percentage of women age 15-49 years who received at least two or more IPT doses during pregnancy -> MICS",
        "indicator": "Percentage of women age 15-49 years who received at least two or more IPT doses during pregnancy",
        "datasource": "MICS",
    },
    {
        "name": "Percentage of women age 15-49 years who received at least two or more IPT doses during pregnancy -> NDHS",
        "indicator": "Percentage of women age 15-49 years who received at least two or more IPT doses during pregnancy",
        "datasource": "NDHS",
    },
    {
        "name": "Percentage of women age 15-49 years who received at least two or more IPT doses during pregnancy -> NHMIS",
        "indicator": "Percentage of women age 15-49 years who received at least two or more IPT doses during pregnancy",
        "datasource": "NHMIS",
    },
    {
        "name": "Percentage of women age 15-49 years who received at least two or more IPT doses during pregnancy -> NMIS",
        "indicator": "Percentage of women age 15-49 years who received at least two or more IPT doses during pregnancy",
        "datasource": "NMIS",
    },
    {
        "name": "Postnatal care coverage (mother) -> MICS",
        "indicator": "Postnatal care coverage (mother)",
        "datasource": "MICS",
    },
    {
        "name": "Postnatal care coverage (mother) -> NARHS",
        "indicator": "Postnatal care coverage (mother)",
        "datasource": "NARHS",
    },
    {
        "name": "Postnatal care coverage (mother) -> NDHS",
        "indicator": "Postnatal care coverage (mother)",
        "datasource": "NDHS",
    },
    {"name": "Prevalence of HIV -> IHME", "indicator": "Prevalence of HIV", "datasource": "IHME"},
    {"name": "Prevalence of HIV -> NAIIS", "indicator": "Prevalence of HIV", "datasource": "NAIIS"},
    {"name": "Prevalence of HIV -> NARHS", "indicator": "Prevalence of HIV", "datasource": "NARHS"},
    {
        "name": "Prevalence of HIV -> NHSPSS",
        "indicator": "Prevalence of HIV",
        "datasource": "NHSPSS",
    },
    {
        "name": "Prevalence of HIV -> UNAIDS",
        "indicator": "Prevalence of HIV",
        "datasource": "UNAIDS",
    },
    {
        "name": "Prevalence of HIV -> WHO-GHO",
        "indicator": "Prevalence of HIV",
        "datasource": "WHO-GHO",
    },
    {
        "name": "Prevalence of HIV -> World Bank",
        "indicator": "Prevalence of HIV",
        "datasource": "World Bank",
    },
    {
        "name": "Prevalence of Symptoms of Acute Respiratory Infection among under five children -> MICS",
        "indicator": "Prevalence of Symptoms of Acute Respiratory Infection among under five children",
        "datasource": "MICS",
    },
    {
        "name": "Prevalence of Symptoms of Acute Respiratory Infection among under five children -> NDHS",
        "indicator": "Prevalence of Symptoms of Acute Respiratory Infection among under five children",
        "datasource": "NDHS",
    },
    {
        "name": "Prevalence of Symptoms of Acute Respiratory Infection among under five children -> NNHS",
        "indicator": "Prevalence of Symptoms of Acute Respiratory Infection among under five children",
        "datasource": "NNHS",
    },
    {
        "name": "Prevalence of children with diarrhoea -> IHME",
        "indicator": "Prevalence of children with diarrhoea",
        "datasource": "IHME",
    },
    {
        "name": "Prevalence of children with diarrhoea -> KDGHS",
        "indicator": "Prevalence of children with diarrhoea",
        "datasource": "KDGHS",
    },
    {
        "name": "Prevalence of children with diarrhoea -> MICS",
        "indicator": "Prevalence of children with diarrhoea",
        "datasource": "MICS",
    },
    {
        "name": "Prevalence of children with diarrhoea -> NDHS",
        "indicator": "Prevalence of children with diarrhoea",
        "datasource": "NDHS",
    },
    {
        "name": "Prevalence of children with diarrhoea -> NNHS",
        "indicator": "Prevalence of children with diarrhoea",
        "datasource": "NNHS",
    },
    {
        "name": "Prevalence of malaria among under five children (microscopy positive) -> IHME",
        "indicator": "Prevalence of malaria among under five children (microscopy positive)",
        "datasource": "IHME",
    },
    {
        "name": "Prevalence of malaria among under five children (microscopy positive) -> NDHS",
        "indicator": "Prevalence of malaria among under five children (microscopy positive)",
        "datasource": "NDHS",
    },
    {
        "name": "Prevalence of malaria among under five children (microscopy positive) -> NMIS",
        "indicator": "Prevalence of malaria among under five children (microscopy positive)",
        "datasource": "NMIS",
    },
    {
        "name": "Prevalence of stunting among under 5 children -> IHME",
        "indicator": "Prevalence of stunting among under 5 children",
        "datasource": "IHME",
    },
    {
        "name": "Prevalence of stunting among under 5 children -> MICS",
        "indicator": "Prevalence of stunting among under 5 children",
        "datasource": "MICS",
    },
    {
        "name": "Prevalence of stunting among under 5 children -> NDHS",
        "indicator": "Prevalence of stunting among under 5 children",
        "datasource": "NDHS",
    },
    {
        "name": "Prevalence of stunting among under 5 children -> NNHS",
        "indicator": "Prevalence of stunting among under 5 children",
        "datasource": "NNHS",
    },
    {
        "name": "Prevalence of stunting among under 5 children -> WHO-GHO",
        "indicator": "Prevalence of stunting among under 5 children",
        "datasource": "WHO-GHO",
    },
    {
        "name": "Prevalence of wasting among under 5 children -> IHME",
        "indicator": "Prevalence of wasting among under 5 children",
        "datasource": "IHME",
    },
    {
        "name": "Prevalence of wasting among under 5 children -> MICS",
        "indicator": "Prevalence of wasting among under 5 children",
        "datasource": "MICS",
    },
    {
        "name": "Prevalence of wasting among under 5 children -> NDHS",
        "indicator": "Prevalence of wasting among under 5 children",
        "datasource": "NDHS",
    },
    {
        "name": "Prevalence of wasting among under 5 children -> NNHS",
        "indicator": "Prevalence of wasting among under 5 children",
        "datasource": "NNHS",
    },
    {
        "name": "Prevalence of wasting among under 5 children -> WHO-GHO",
        "indicator": "Prevalence of wasting among under 5 children",
        "datasource": "WHO-GHO",
    },
    {
        "name": "Proportion of children under 5 with ARI who received antibiotics -> MICS",
        "indicator": "Proportion of children under 5 with ARI who received antibiotics",
        "datasource": "MICS",
    },
    {
        "name": "Proportion of children under 5 with ARI who received antibiotics -> NDHS",
        "indicator": "Proportion of children under 5 with ARI who received antibiotics",
        "datasource": "NDHS",
    },
    {
        "name": "Proportion of children under 5 with ARI who received antibiotics -> NNHS",
        "indicator": "Proportion of children under 5 with ARI who received antibiotics",
        "datasource": "NNHS",
    },
    {
        "name": "Proportion of children under 5 with ARI who received antibiotics -> WHO-GHO",
        "indicator": "Proportion of children under 5 with ARI who received antibiotics",
        "datasource": "WHO-GHO",
    },
    {
        "name": "Skilled attendance at delivery or birth -> IHME",
        "indicator": "Skilled attendance at delivery or birth",
        "datasource": "IHME",
    },
    {
        "name": "Skilled attendance at delivery or birth -> KDGHS",
        "indicator": "Skilled attendance at delivery or birth",
        "datasource": "KDGHS",
    },
    {
        "name": "Skilled attendance at delivery or birth -> MICS",
        "indicator": "Skilled attendance at delivery or birth",
        "datasource": "MICS",
    },
    {
        "name": "Skilled attendance at delivery or birth -> NARHS",
        "indicator": "Skilled attendance at delivery or birth",
        "datasource": "NARHS",
    },
    {
        "name": "Skilled attendance at delivery or birth -> NDHS",
        "indicator": "Skilled attendance at delivery or birth",
        "datasource": "NDHS",
    },
    {
        "name": "Skilled attendance at delivery or birth -> NHMIS",
        "indicator": "Skilled attendance at delivery or birth",
        "datasource": "NHMIS",
    },
    {
        "name": "Skilled attendance at delivery or birth -> NNHS",
        "indicator": "Skilled attendance at delivery or birth",
        "datasource": "NNHS",
    },
    {
        "name": "Skilled attendance at delivery or birth -> WHO-GHO",
        "indicator": "Skilled attendance at delivery or birth",
        "datasource": "WHO-GHO",
    },
    {
        "name": "Skilled attendance at delivery or birth -> World Bank",
        "indicator": "Skilled attendance at delivery or birth",
        "datasource": "World Bank",
    },
    {
        "name": "Total fertility rate -> IHME",
        "indicator": "Total fertility rate",
        "datasource": "IHME",
    },
    {
        "name": "Total fertility rate -> MICS",
        "indicator": "Total fertility rate",
        "datasource": "MICS",
    },
    {
        "name": "Total fertility rate -> NDHS",
        "indicator": "Total fertility rate",
        "datasource": "NDHS",
    },
    {
        "name": "Total fertility rate -> NHMIS",
        "indicator": "Total fertility rate",
        "datasource": "NHMIS",
    },
    {
        "name": "Total fertility rate -> NMIS",
        "indicator": "Total fertility rate",
        "datasource": "NMIS",
    },
    {
        "name": "Total fertility rate -> WHO-GHO",
        "indicator": "Total fertility rate",
        "datasource": "WHO-GHO",
    },
    {
        "name": "Total fertility rate -> World Bank",
        "indicator": "Total fertility rate",
        "datasource": "World Bank",
    },
    {
        "name": "Under 5 Mortality rate -> IHME",
        "indicator": "Under 5 Mortality rate",
        "datasource": "IHME",
    },
    {
        "name": "Under 5 Mortality rate -> KDGHS",
        "indicator": "Under 5 Mortality rate",
        "datasource": "KDGHS",
    },
    {
        "name": "Under 5 Mortality rate -> MICS",
        "indicator": "Under 5 Mortality rate",
        "datasource": "MICS",
    },
    {
        "name": "Under 5 Mortality rate -> NARHS",
        "indicator": "Under 5 Mortality rate",
        "datasource": "NARHS",
    },
    {
        "name": "Under 5 Mortality rate -> NDHS",
        "indicator": "Under 5 Mortality rate",
        "datasource": "NDHS",
    },
    {
        "name": "Under 5 Mortality rate -> NHMIS",
        "indicator": "Under 5 Mortality rate",
        "datasource": "NHMIS",
    },
    {
        "name": "Under 5 Mortality rate -> NMIS",
        "indicator": "Under 5 Mortality rate",
        "datasource": "NMIS",
    },
    {
        "name": "Under 5 Mortality rate -> WHO-GHO",
        "indicator": "Under 5 Mortality rate",
        "datasource": "WHO-GHO",
    },
    {
        "name": "Under 5 Mortality rate -> World Bank",
        "indicator": "Under 5 Mortality rate",
        "datasource": "World Bank",
    },
    {
        "name": "Underweight prevalence among under 5 children -> IHME",
        "indicator": "Underweight prevalence among under 5 children",
        "datasource": "IHME",
    },
    {
        "name": "Underweight prevalence among under 5 children -> MICS",
        "indicator": "Underweight prevalence among under 5 children",
        "datasource": "MICS",
    },
    {
        "name": "Underweight prevalence among under 5 children -> NDHS",
        "indicator": "Underweight prevalence among under 5 children",
        "datasource": "NDHS",
    },
    {
        "name": "Underweight prevalence among under 5 children -> NHMIS",
        "indicator": "Underweight prevalence among under 5 children",
        "datasource": "NHMIS",
    },
    {
        "name": "Underweight prevalence among under 5 children -> NNHS",
        "indicator": "Underweight prevalence among under 5 children",
        "datasource": "NNHS",
    },
    {
        "name": "Underweight prevalence among under 5 children -> WHO-GHO",
        "indicator": "Underweight prevalence among under 5 children",
        "datasource": "WHO-GHO",
    },
    {
        "name": "Unmet need for family planning -> IHME",
        "indicator": "Unmet need for family planning",
        "datasource": "IHME",
    },
    {
        "name": "Unmet need for family planning -> MICS",
        "indicator": "Unmet need for family planning",
        "datasource": "MICS",
    },
    {
        "name": "Unmet need for family planning -> NDHS",
        "indicator": "Unmet need for family planning",
        "datasource": "NDHS",
    },
    {
        "name": "Unmet need for family planning -> WHO-GHO",
        "indicator": "Unmet need for family planning",
        "datasource": "WHO-GHO",
    },
    {
        "name": "Vitamin A supplementation coverage -> MICS",
        "indicator": "Vitamin A supplementation coverage",
        "datasource": "MICS",
    },
    {
        "name": "Vitamin A supplementation coverage -> NDHS",
        "indicator": "Vitamin A supplementation coverage",
        "datasource": "NDHS",
    },
    {
        "name": "Vitamin A supplementation coverage -> NNHS",
        "indicator": "Vitamin A supplementation coverage",
        "datasource": "NNHS",
    },
    {
        "name": "Vitamin A supplementation coverage -> WHO-GHO",
        "indicator": "Vitamin A supplementation coverage",
        "datasource": "WHO-GHO",
    },
]


def run_process():
    """
    run the data-processing
    """
    # ===================================
    # LOAD OPTIMIZED DATA QUERY CACHES
    # ===================================
    converter_utils.helper_cache_data_processor_refrences()

    # the response data to be serialized
    data_row_structure = []

    # the proccesing temp data-cache
    data_res_model_fields = []

    # pre populate data-caches
    # initialize the the lists structure
    for index in range(0, len(response_model)):
        data_row_structure.append("")

        data_res_model_fields.append([])

    response_data = []

    try:
        # ================================
        # RUN QUERIES
        # ================================

        # LOCATIONS
        data_location_states = converter_utils.helper_extract_locations_nigerian_states()

        # DATA
        # a single request for all data in the data_table
        data_all = main_models.Data.objects.all().select_related("datasource", "indicator")

        # ================================
        # PARSE QUERY DATA
        # ================================

        # cycle through the response-headers for indicators and datasources that exists
        # for those that exist cycle throuh the data for their data-value in the database
        # and add to the list of data_res_model_fields
        converter_utils.helper_populate_indicator_datasource_field(
            data_res_model_fields, response_model, data_all
        )

        # ================================
        # PACKAGE RESPONSE
        # ================================

        # CREATE THE FIRST data_item
        data_headings = []
        for heading in response_model:
            data_headings.append(heading["name"])
        response_data.append(data_headings)

        def func_create_rows_for_national_data_within_a_period(param_period):
            """
            create rows of data.state_id=1(nigeria),location_level=1(countries),country=1(nigeria)

            Args:
                :param param_period:int
            Returns:
                :rtype: Void
            """
            # shallow copy the initialized list structure
            data_row = data_row_structure.copy()

            data_row[0] = period  # index 0
            data_row[1] = "National"  # index 1

            for index in range(2, len(data_row)):  # index 2-end
                data_row[index] = converter_utils.helper_extract_data_value_by_location_and_period(
                    data_res_model_fields[index],
                    param_period,
                    converter_utils.helper_get_location_country_nigeria().id,
                )

            response_data.append(data_row)

        def func_create_rows_for_state_within_a_period(param_period):
            """
            create rows of data.state_id=1 in the period range

            Args:
                :param param_period:int
            Returns:
                :rtype: Void
            """

            for state in data_location_states:
                # shallow copy the initialized list structure
                data_row = data_row_structure.copy()

                data_row[0] = period  # index 0
                data_row[1] = state.name  # index 1

                for index in range(2, len(data_row)):  # index 2-end
                    data_row[index] = (
                        converter_utils.helper_extract_data_value_by_location_and_period(
                            data_res_model_fields[index], param_period, state.id
                        )
                    )

                response_data.append(data_row)

        # CREATE THE rows for national-level-data from 1964 to 1989
        for period in range(PERIOD_NATIONAL["start"], PERIOD_NATIONAL["end"]):
            func_create_rows_for_national_data_within_a_period(period)

        # CREATE THE rows for location-level-data from 1990 to
        for period in range(PERIOD_STATES["start"], PERIOD_STATES["end"]):
            func_create_rows_for_national_data_within_a_period(period)

            func_create_rows_for_state_within_a_period(period)

        return response_data

    except Exception as e:
        # LOG
        utils_logger.log_print("", str(e), param_oneline=True)

        traceback.print_tb(e.__traceback__)

        return response_data
