import re

cv_trader_quant_data = """
**SUMMARY**
Experienced trader and top quantitative student with a strong track record managing $200M+ AUM in North American and Asian index options. Skilled in execution trading, market microstructure, and AI-driven sentiment analysis. Combining data mining and fundamental analysis to identify trading opportunities. Eligible to work in Canada with citizenship assurance.

**PROFESSIONAL EXPERIENCE**
Washington University in St. Louis, Olin Business School	St. Louis, MO, USA
Research Assistant	May 2024 - Present
Overview: Data scientist in processing novel databases, fine-tuning sentiment analysis models, and AI-LLM market forecasting
-	Developed a Selenium web scraper to extract data from social media and news databases, improved sentiment classification through BERT model fine-tuning, transforming it into a key resource for quantitative research
-	Cleansed a novel, century-long, 400,000-entry United States' congressional hearing database for market insights
-	Drafted a Stata pipeline for processing confidential SEC data, facilitating efficient handling of large-scale confidential dataset
Privium Fund Management	Hong Kong
Portfolio Manager	Apr 2022 - Dec 2022
Overview: Co-managed US$ 200M AUM options selling strategy, overseeing algorithmic trading and risk management
-	Executed options selling strategy on index options, minimizing slippage and maximizing premiums with algorithmic trading
-	Analyzed volatility skew to identify mispriced options and adjusted positions for value opportunities
-	Applied risk models (Barra, Black-Litterman, Axioma, Greeks) for portfolio optimization and ensuring risk alignment
-	Managed liquidity and order book dynamics to reduce slippage and optimize risk-adjusted returns
-	Performed portfolio stress testing under various market scenarios to ensure robustness across $200M in managed assets
Yong Rong Asset	Hong Kong
Junior Trader	Jun 2021 - Jan 2022
Overview: Research-focused buy-side trader at a fundamental high-conviction macro sub-fund
-	Participated in trading activities for a high-conviction sub-fund with an AUM of $30M, focused on high-growth technology companies in North American equity markets. Maintained the firm's trading and reporting scripts to support execution
-	Maintained trading and reporting scripts to support accurate and timely trade execution
-	Produced comprehensive research memos for U.S. space exploration, remote sensing, and Hong Kong machinery sectors
Peak Global Investments	Hong Kong
Private Equity Intern	Sep 2020 - May 2021
Overview: Research, due diligence-focused intern while contributing to the firm's crypto and DeFi proprietary trading strategies
-	Researched cryptocurrency exchanges across Asia and Europe, liaised with senior executives to prepare for acquisitions
-	Collaborated with world's largest crypto exchange, utilized API to assess targets' trading volumes and their authenticity

**EDUCATION**
Washington University in St. Louis (WashU)	St. Louis, MO, USA
M.S. in Finance, Quantitative	Sep 2023 - Dec 2024 (Expected)
-	GPA: 3.95/4.00, Rank 2/80
-	Honors: All-semester Dean's List, Beta Gamma Sigma Award, Charles F. Knight Scholar (Expected)
-	Coursework: Advanced Continuous-Time Finance (Ph.D.), Advanced Derivative Securities, Fixed Income Derivatives, Machine Learning, Mathematical Finance, Data Analysis, Database Design and SQL, Quantitative Risk Management
The University of Hong Kong (HKU)	Hong Kong
B.S. in Economics and Finance	Sep 2017 - May 2021
-	GPA: 3.45/4.00, Rank 35%
-	Admitted based on achieving a top 0.4% province-ranking (143rd / 411,897) in National College Entrance Exam (Gaokao)
Institut d'Études Politiques de Paris (Sciences Po)	Paris, France
Scholarship-Awarded Exchange Student	Jan 2020 - May 2020
-	GPA: 17/20, Awarded HKU Reaching Out Award (C.V. Starr Scholarship)

**SKILLS**
Teaching	TA for: Options, Futures and Derivative Securities (Undergraduate); Behavioral Finance (Graduate)
Research	Data Matching for PEVC-backed Companies - Cornell University RA under Prof. Minmo Gahng; The Causal Impact of Fiscal Shocks - WashU RA under Prof. William Cassidy
Volunteering	NGO Marketing Director, Soap Cycling HKU; Volunteer Teacher, Beyond the Pivot HKU;
Organizations	Director of Public Relations, XGravity Outdoors Club HKU

**SKILLS & PERSONAL**
Certificates	CFA Level II Candidate, FRM Level I Candidate, HKSFC Type-9 Asset Management License
Technical	Python, R, Stata, SQL, Git, MATLAB, VBA, LaTeX, Bloomberg, Capital IQ, Microsoft Office, Tableau
Languages	Mandarin (Native), English (Fluent, IELTS 8.0), Cantonese (Intermediate)
Work Permits	Hong Kong SAR (Nationality), Canada (OWP with Citizenship Assurance), USA (OPT)
"""

cv_research = """
**EDUCATION**
Washington University in St. Louis	St. Louis, MO
M.S. in Finance, Quantitative	Sep 2023 - Dec 2024 (Expected)
-	GPA: 3.95/4.00
-	Honors: Beta Gamma Sigma, Charles F. Knight Scholar (Expected)
-	Coursework: Advanced Continuous-Time Finance (Ph.D. Level), Advanced Derivative Securities, Fixed Income Derivatives, Machine Learning, Mathematical Finance, Data Analysis for Investments, Database Design and SQL 
The University of Hong Kong	Hong Kong
B.S. in Economics and Finance	Sep 2017 - May 2021
-	GPA: 3.45/4.00 (WES-verified), Rank top 40%
-	Honors: Second Class Honors Division One, HKU Reaching Out Award (C.V. Starr Scholarship)
-	Coursework: Multivariable Calculus, Investments and Portfolio Analysis, Hedge Funds: Strategies, Business Management
Institut d'Études Politiques de Paris (Sciences Po)	Paris, France
Exchange Student	Jan 2020 - May 2020
-	GPA: 17/20

**PROFESSIONAL EXPERIENCE**
Privium Fund Management	Hong Kong
Assistant Portfolio Manager - Execution Trading	Apr 2022 - Dec 2022
-	Executed options selling strategy on index options, minimizing slippage and maximizing premiums with algorithmic trading
-	Analyzed volatility skew to identify mispriced options and adjusted positions for value opportunities
-	Applied risk models (Barra, Black-Litterman, Axioma, Greeks) for portfolio optimization and ensuring risk alignment
-	Managed liquidity and order book dynamics to reduce slippage and optimize risk-adjusted returns
-	Performed portfolio stress testing under various market scenarios to ensure robustness across $200M in managed assets
Yong Rong Asset	Hong Kong
Junior Trader	Jun 2021 - Jan 2022
-	Participated in trading activities for a high-conviction sub-fund with an AUM of $30M, focused on high-growth technology companies in North American equity markets. Maintained the firm's trading and reporting scripts to support execution
-	Maintained trading and reporting scripts to support accurate and timely trade execution
-	Produced comprehensive research memos for U.S. space exploration, remote sensing, and Hong Kong machinery sectors
Peak Global Investments	Hong Kong
Private Equity & Venture Capital Intern	Sep 2020 - May 2021
-	Researched cryptocurrency exchanges across Asia and Europe, liaised with senior executives to prepare for acquisitions
-	Conducted extensive financial analysis and due diligence on potential investment opportunities in different industries
-	Collaborated with world's largest crypto exchange, utilized API to assess targets' trading volumes and their authenticity

**RESEARCH EXPERIENCE**
Text-based Analysis of Fiscal and Monetary Policy Interaction Using Novel Dataset	St. Louis, MO
Washington University in St. Louis, under Prof. William Cassidy & Jingoo Kwon	Oct 2023 - Present
-	Developed a Python-based pipeline to clean and process over 400,000 rows of novel scanned PDF dataset, correcting line-break errors, resolving missing and inconsistent data, and verifying key speaker identities using historical context
-	Fine-tuned BERT topic model and sub-models (UMAP, HDBSCAN, cTF-IDF, Representation), identified key themes in fiscal and monetary discussions during congressional hearings, enhancing sentiment analysis and label accuracy
Data Matching for PEVC-backed Companies: GitHub and SEC Data	Ithaca, NY (Remote)
Cornell University, under Prof. Minmo Gahng & Prof. Michael Ewens	Apr 2024 - Present
-	Filtered and identified U.S.-based companies from scraped GitHub data, using a combination of exact matching, fuzzy matching, and an 800-line custom TF-IDF matching codes to ensure high accuracy in company identification
-	Created and organized two critical Stata data frames (PE and LP) from a sample confidential SEC dataset provided by the professor's co-author, focusing on various time intervals (yearly, quarterly, monthly) for fund-specific analysis
The Causal Impact of Fiscal Shocks	St. Louis, MO
Washington University in St. Louis, under Prof. William Cassidy & Prof. Aditya Chaudhry	Apr 2024 - Present
-	Scraped and processed historical news data related to UK budget announcements, using keyword searches to identify relevant reports and categorize them as bullish or bearish 
-	Performed multiple regression analyses to investigate the causal relationship between sentiment and asset price changes, controlling for market volatility, macroeconomic conditions, and time-lag effects 

**EADERSHIP & ACTIVITIES**
Teaching	TA at Washington University in St. Louis: Options, Futures and Derivative Securities (Undergraduate Course); Behavioral Finance (Gradate Course)
Volunteering	NGO Marketing Director, Soap Cycling HKU; Volunteer Teacher, Beyond the Pivot HKU
Organizations	Director of Public Relations, XGravity Outdoors Club HKU

**SKILLS & PERSONAL**
Certificates	CFA Level I, HKSFC Asset Management License (Type 9)
Programming	Advanced in Python, R, SQL, VBA, LaTeX; Intermediate in STATA, MATLAB
Software	SPSS, Markdown, Bloomberg Terminal, Capital IQ, Tableau, Microsoft Office
"""

cv_equity_research = """
**PROFESSIONAL SUMMARY**
RResearcher with a strong foundation in fundamental analysis, specializing in evaluating company performance, industry trends, and financial statements. Recently integrated AI-LLM tools to enhance traditional research methods, using advanced data processing techniques to extract timely insights from unstructured data such as earnings reports and regulatory filings. Combination of in-depth fundamental research and technology enables faster, more accurate assessments of market movements.

**EXPERIENCE**
Washington University in St. Louis, Olin Business School	St. Louis, MO, USA
Research Assistant (Post Grant), Prof. William Cassidy	Oct 2023 - Present
-	Applied time-series analysis and event-driven models to explore the direct impact of UK budget announcements on UK's monetary policy, bypassing inflation metrics, focusing on the political influence on monetary decisions
-	Utilized AI-LLM and BERT models to identify missed speaker transitions where new speakers were not properly segmented
-	Leveraged a pre-existing list of U.S. Congress members to assist in speaker identification and applied LLMs to detect inconsistencies in speech patterns, improving text accuracy by 20% and enhancing the reliability of downstream analysis
Cornell University, S.C. Johnson School of Business	Ithaca, NY, USA (Remote)
Research Assistant, Prof. Minmo Gahng	Mar 2024 - Present
-	Filtered U.S.-based companies from GitHub contributors and matched them with PEVC-backed firms using TF-IDF techniques, enabling accurate alignment of tens of thousands of data rows from multiple sources
-	Reviewed methodologies from related fields and assessed their applicability to PEVC research, conducted regression analysis using linear and logistic models, ensuring model validity through hypothesis testing and multicollinearity checks
Privium Fund Management	Hong Kong
Assistant Portfolio Manager	Apr 2022 - Dec 2022
-	Executed options selling strategy across North American and Asian index options with an AUM of $200M, utilizing algorithmic trading to minimize slippage and maximize premium collection, achieving an average annualized return of 8%+
-	Applied models such as Barra, Black-Litterman and Axioma for risk analysis and portfolio optimization, managing long/short positions in underlying assets to balance portfolio Greeks, ensuring alignment with risk management guidelines
-	Performed portfolio stress testing under various market scenarios to ensure robustness across $200M in managed assets
Yong Rong Asset	Hong Kong
Junior Trader and Research Analyst	Jun 2021 - Jan 2022
-	Conducted covert investigations into a Hong Kong-listed machinery company by utilizing disguised client order monitoring, satellite imagery analysis, government news extraction. Uncovered hidden insights, assisted with detailed financial statement forecast, leading to the identification of a 27% upside potential, which was realized within one month
Peak Global Investments	Hong Kong
Private Equity Intern	Sep 2020 - May 2021
-	Facilitated detailed research and analysis on dozens of crypto exchanges and new agencies across Asia-Pacific and European regions, evaluating their trading volumes, management teams, and financials. Organized and led multiple management interviews, providing strategic insights to support subsequent acquisition decisions for selected companies
CMBC Capital	Hong Kong
Corporate Finance Intern	Jun 2020 - Aug 2020
-	Assisted financial due diligence and assisted in the valuation of companies preparing for IPO and Leveraged Borrowing, analyzing financial statements and market conditions to support pricing strategies and ensure regulatory compliance


**EDUCATION**
Washington University in St. Louis (WashU)	St. Louis, MO, USA
M.S. in Finance, Quantitative	Sep 2023 - Dec 2024 (Expected)
-	GPA: 3.95/4.00, Rank 2/80
-	Honors: All-semester Dean's List, Beta Gamma Sigma Award, Charles F. Knight Scholar (Expected)
The University of Hong Kong (HKU)	Hong Kong
B.S. in Economics and Finance	Sep 2017 - May 2021
Institut d'Études Politiques de Paris (Sciences Po)	Paris, France
Scholarship-Awarded Exchange Student	Jan 2020 - May 2020

**LEADERSHIP & ACTIVITIES**
Teaching	TA for: Options, Futures and Derivative Securities (Undergraduate); Behavioral Finance (Graduate)
Volunteering	NGO Marketing Director, Soap Cycling HKU; Volunteer Teacher, Beyond the Pivot HKU;

**SKILLS & PERSONAL**
Certificates	CFA Level II Candidate, FRM Level I Candidate, HKSFC Type-9 Asset Management License
Technical	Python, R, Stata, SQL, Git, MATLAB, VBA, LaTeX, Bloomberg, Capital IQ, Microsoft Office, Tableau
Languages	Mandarin (Native), English (Fluent, IELTS 8.0), Cantonese (Intermediate)
Work Permits	Hong Kong SAR (Nationality), Canada (OWP with Citizenship Assurance), USA (OPT)
"""

cv_pan_finance = """
**SUMMARY**
Professional and strong background in financial analysis, forecasting, and data-driven decision-making. Highly detail-oriented and skilled in identifying data anomalies and trends ahead of time to provide actionable insights. Experienced in managing funds and portfolio analysis, ensuring accurate reporting and budget forecasting. Eligible to work in Canada with citizenship assurance. 

**PROFESSIONAL EXPERIENCE**
Washington University in St. Louis, Olin Business School	St. Louis, MO, USA
Research Assistant	May 2024 - Present
Overview: Data scientist in team in charge of dataset processing, pipeline development and data analysis and forecasting
-	Developed a Selenium-based automation to detect and correct inconsistencies in a 60,000-entry century-long database such as misaligned lines and outdated terminologies, which later became a key resource for ongoing quantitative research
-	Utilized multiple AI-LLMs to forecast market movements by processing unstructured text data such as earnings reports and regulatory filings. Improved decision-making in highly volatile sectors, resulting in more accurate trade timing
-	Finetuned BERT models to analyze scraped financial news and social media, identifying market themes and sentiment shifts
Privium Fund Management	Hong Kong
Assistant Portfolio Manager	Apr 2022 - Nov 2022
Overview: Co-managed US$ 200M AUM options selling strategy, overseeing trade settlement and cash management
-	Developed a Python-based pipeline to automate trade confirmations from execution and prime brokers, reconciling Excel data with the internal SS&C Eze system and flagging discrepancies for manual review to streamline operational workflows
-	Identified early trends, irregularities and anomalies in fund's financial data through Dupont Analysis, providing proactive recommendations to management to mitigate potential risks and improve financial reporting accuracy
-	Performed portfolio stress testing under various market scenarios to ensure robustness across $200M in managed assets
Yong Rong Asset	Hong Kong
Junior Trader	Jun 2021 - Nov 2021
Overview: Buy-side trader at fundamental high-conviction macro fund, also charging reconciliation and monitoring
-	Gained deep expertise in derivatives pricing models and payoff structures, collaborated with execution brokers to ensure accurate trade execution by verifying trade details, including pricing, volumes, and underlying assets
-	Managed daily PnL calculations and accruals, ensuring accurate financial reporting and reconciliation with prime broker records, contributing to budget forecasting and alignment of statements of profit and loss and balance sheets
Peak Global Investments	Hong Kong
Private Equity Intern	Sep 2020 - May 2021
-	Conducted comprehensive financial analysis and due diligence for potential acquisitions, including cash flow assessments, financial ratio analysis, and cost control evaluations, providing actionable insights to support strategic decision-making

**EDUCATION**
Washington University in St. Louis (WashU)	St. Louis, MO, USA
M.S. in Finance, Quantitative	Sep 2023 - Dec 2024 (Expected)
-	GPA: 3.95/4.00, Rank 2/80
-	Honors: All-semester Dean's List, Beta Gamma Sigma Award, Charles F. Knight Scholar (Expected)
-	Coursework: Advanced Derivatives, Database Design and SQL, Mathematical Finance, Financial Analysis
The University of Hong Kong (HKU)	Hong Kong
B.S. in Economics and Finance	Sep 2017 - May 2021
-	GPA: 3.45/4.00, Rank 35%
-	Admitted based on achieving a top 0.4% province-ranking (143rd / 411,897) in National College Entrance Exam (Gaokao)
-	Coursework: Hedge Fund Strategies, Derivatives, Financial Statement Modelling, International Finance
Institut d'Études Politiques de Paris (Sciences Po)	Paris, France
Scholarship-Awarded Exchange Student	Jan 2020 - May 2020
-	GPA: 17/20, Awarded HKU Reaching Out Award (C.V. Starr Scholarship)

**LEADERSHIP & ACTIVITIES**
Teaching	TA for: Options, Futures and Derivative Securities (Undergraduate); Behavioral Finance (Graduate)
Research	Data Matching for PEVC-backed Companies - Cornell University RA under Prof. Minmo Gahng; The Causal Impact of Fiscal Shocks - WashU RA under Prof. William Cassidy
Volunteering	NGO Marketing Director, Soap Cycling HKU; Volunteer Teacher, Beyond the Pivot HKU;
Organizations	Director of Public Relations, XGravity Outdoors Club HKU

**SKILLS & PERSONAL**
Certificates	CFA Level II Candidate, FRM Level I Candidate, HKSFC Type-9 Asset Management License
Technical	Python, R, Stata, SQL, Git, MATLAB, VBA, LaTeX, Bloomberg, Capital IQ, Microsoft Office, Tableau
Languages	Mandarin (Native), English (Fluent, IELTS 8.0), Cantonese (Intermediate)
Work Permits	Hong Kong SAR (Nationality), Canada (OWP with Citizenship Assurance), USA (OPT)

"""

cv_ibd = """
**SUMMARY**
Finance professional with experience in corporate finance and investment banking. Experienced in IPO projects, financial due diligence, and performed company valuations. Strong analytical skills developed through internships at CMBC Capital and Peak Global Investments, and a top Quantitative Finance student at Washington University in St. Louis with a GPA 3.95/4.00.

**PROFESSIONAL EXPERIENCE**
Washington University in St. Louis, Olin Business School	St. Louis, MO, USA
Data Scientist (Post Grant)	May 2024 - Present
-	Utilized multiple AI-LLMs to forecast market movements by processing unstructured text data such as earnings reports and regulatory filings. Improved decision-making in highly volatile sectors, resulting in more accurate trade timing
-	Developed a pipeline to detect and correct inconsistencies in a century-long database such as misaligned lines, missing values, and outdated terminologies, the enhanced dataset became a key resource for ongoing quantitative research
Privium Fund Management	Hong Kong
Assistant Portfolio Manager	Apr 2022 - Dec 2022
-	Executed options selling strategy across North American and Asian index options with an AUM of $200M, utilizing algorithmic trading to minimize slippage and maximize premium collection, achieving an average annualized return of 8%+
-	Applied models such as Barra, Black-Litterman and Axioma for risk analysis and portfolio optimization, managing long/short positions in underlying assets to balance portfolio Greeks, ensuring alignment with risk management guidelines
Yong Rong Asset	Hong Kong
Junior Trader and Research Analyst	Jun 2021 - Jan 2022
-	Conducted covert investigations into a Hong Kong-listed machinery company by utilizing disguised client order monitoring, satellite imagery analysis, government news extraction. Uncovered hidden insights, leading to the identification of a 27% upside potential, which was realized within one month
-	Undertook in-depth research on the U.S. emerging aerospace market, focusing on SPAC mergers, remote sensing satellite, and rocket industries, engaged with industry experts and participated in over ten earnings calls to gather primary insights
Peak Global Investments	Hong Kong
Private Equity Intern	Sep 2020 - May 2021
-	Facilitated detailed research and analysis on dozens of crypto exchanges and new agencies across Asia-Pacific and European regions, evaluating their trading volumes, management teams, and financials. Organized and led multiple management interviews, providing strategic insights to support subsequent acquisition decisions for selected companies
CMBC Capital	Hong Kong
Investment Banking Summer Analyst	Jun 2020 - Aug 2020
-	Deeply involved in three IPO projects sponsored by the firm: independently drafted pitchbooks and actively participated in subsequent stages, including coordination with law firms and target companies, roadshow preparations and bookbuilding
-	Assisted financial due diligence and assisted in the valuation of companies preparing for IPO and Leveraged Borrowing, analyzing financial statements and market conditions to support pricing strategies and ensure regulatory compliance

**EDUCATION**
Washington University in St. Louis (WashU)	St. Louis, MO, USA
M.S. in Finance, Quantitative	Sep 2023 - Dec 2024 (Expected)
-	GPA: 3.95/4.00, Rank 2/80
-	Honors: All-semester Dean's List, Beta Gamma Sigma Award, Charles F. Knight Scholar (Expected)
The University of Hong Kong (HKU)	Hong Kong
B.S. in Economics and Finance	Sep 2017 - May 2021
-	GPA: 3.45/4.00, Rank 35%
-	Admitted based on achieving a top 0.4% province-ranking (143rd / 411,897) in National College Entrance Exam (Gaokao)
Institut d'Études Politiques de Paris (Sciences Po)	Paris, France
Scholarship-Awarded Exchange Student	Jan 2020 - May 2020
-	GPA: 17/20, Awarded HKU Reaching Out Award (C.V. Starr Scholarship)

**LEADERSHIP & ACTIVITIES**
Teaching	TA for: Options, Futures and Derivative Securities (Undergraduate); Behavioral Finance (Graduate)
Research	Data Matching for PEVC-backed Companies - Cornell University RA under Prof. Minmo Gahng; The Causal Impact of Fiscal Shocks - WashU RA under Prof. William Cassidy
Volunteering	NGO Marketing Director, Soap Cycling HKU; Volunteer Teacher, Beyond the Pivot HKU;

**SKILLS & PERSONAL**
Certificates	CFA Level II Candidate, FRM Level I Candidate, HKSFC Type-9 Asset Management License
Technical	Python, R, Stata, SQL, Git, MATLAB, VBA, LaTeX, Bloomberg, Capital IQ, Microsoft Office, Tableau
Languages	Mandarin (Native), English (Fluent, IELTS 8.0), Cantonese (Intermediate)
Work Permits	Hong Kong SAR (Nationality), Canada (OWP with Citizenship Assurance), USA (OPT)
"""

cv_operation = """
**SUMMARY**
Experienced in fund operations with a focus on daily trade reconciliation, PnL calculation, and NAV accuracy, brought expertise in managing liquidity, trade execution, and operational workflows. Successfully automated key processes with advanced proficiency in Python and AI-LLM models, including trade confirmations and data reconciliation, streamlining operational efficiency and reducing manual errors. Track record in valued gained through precise execution and automation solutions.

**PROFESSIONAL EXPERIENCE**
Washington University in St. Louis, Olin Business School	St. Louis, MO, USA
Research Assistant	May 2024 - Present
Overview: Data scientist in team in charge of dataset processing, pipeline development and data analysis and forecasting
-	Developed a Selenium-based automation to detect and correct inconsistencies in a 60,000-entry century-long database such as misaligned lines and outdated terminologies, which later became a key resource for ongoing quantitative research
-	Cleansed a novel, century-long, 400,000-entry United States' congressional hearing database for market insights
-	Drafted a Stata pipeline for processing confidential SEC data, facilitating efficient handling of large-scale confidential dataset
Privium Fund Management	Hong Kong
Portfolio Manager	Apr 2022 - Nov 2022
Overview: Co-managed US$ 200M AUM options selling strategy, overseeing trading, risk management and operation matters
-	Executed options selling strategy, utilizing algorithmic trading to minimize slippage and maximize premium collection
-	Managed liquidity and order book dynamics to control slippage and market impact, while optimizing risk-adjusted returns
-	Developed a Python-based pipeline to automate trade confirmations on SS&C Eze from execution traders, merging Excel data with the internal system and flagging discrepancies for manual review to streamline operational workflows
-	Gained expertise in derivatives pricing models and payoff structures, liaised with counterparties to ensure accurate trade execution by verifying trade details, including pricing, volumes, and assets
Yong Rong Asset	Hong Kong
Junior Trader	Jul 2021 - Nov 2021
Overview: Buy-side trader at fundamental high-conviction macro fund, also in charge trade settlement and cash management
-	Handled high-risk trades in high-growth tech stocks, managed trade orders, optimized execution through market analysis
-	Collaborated with fund accountants to manage and account for accrued expenses, reconciled fund records with prime broker reports, and calculated trading PnL. Ensured accurate NAV calculations and consistent alignment with market data
Peak Global Investments	Hong Kong
Private Equity Intern	Sep 2020 - May 2021
Overview: Research, due diligence-focused intern while contributing to the firm's proprietary trading strategies
-	Researched cryptocurrency exchanges across Asia and Europe, liaised with senior executives to prepare for acquisitions
-	Conducted extensive financial analysis and due diligence on potential investment opportunities in different industries

**EDUCATION**
Washington University in St. Louis (WashU)	St. Louis, MO, USA
M.S. in Finance, Quantitative	Sep 2023 - Dec 2024 (Expected)
-	GPA: 3.95/4.00, Rank 2/80
-	Honors: All-semester Dean's List, Beta Gamma Sigma Award, Charles F. Knight Scholar (Expected)
-	Coursework: Advanced Continuous-Time Finance (Ph.D.), Advanced Derivative Securities, Fixed Income Derivatives, Machine Learning, Mathematical Finance, Data Analysis, Database Design and SQL, Quantitative Risk Management
The University of Hong Kong (HKU)	Hong Kong
B.S. in Economics and Finance	Sep 2017 - May 2021
-	GPA: 3.45/4.00, Rank 35%
-	Admitted based on achieving a top 0.4% province-ranking (143rd / 411,897) in National College Entrance Exam (Gaokao)
Institut d'Études Politiques de Paris (Sciences Po)	Paris, France
Scholarship-Awarded Exchange Student	Jan 2020 - May 2020
-	GPA: 17/20, Awarded HKU Reaching Out Award (C.V. Starr Scholarship)

**LEADERSHIP & ACTIVITIES**
Teaching	TA for: Options, Futures and Derivative Securities (Undergraduate); Behavioral Finance (Graduate)
Research	Data Matching for PEVC-backed Companies - Cornell University RA under Prof. Minmo Gahng; The Causal Impact of Fiscal Shocks - WashU RA under Prof. William Cassidy
Volunteering	NGO Marketing Director, Soap Cycling HKU; Volunteer Teacher, Beyond the Pivot HKU;

**SKILLS & PERSONAL**
Certificates	CFA Level II Candidate, FRM Level I Candidate, HKSFC Type-9 Asset Management License
Technical	Python, R, Stata, SQL, Git, MATLAB, VBA, LaTeX, Bloomberg, Capital IQ, Microsoft Office, Tableau
Languages	Mandarin (Native), English (Fluent, IELTS 8.0), Cantonese (Intermediate)
Work Permits	Hong Kong SAR (Nationality), Canada (OWP with Citizenship Assurance), USA (OPT)

"""

cv_risk = """
**SUMMARY**
Top-performing quantitative finance professional with a 3.95/4.00 GPA. Proven track record in applying advanced models like GARCH and VaR for market risk assessment. Skilled in automating data processing, performing in-depth due diligence, and enhancing decision-making through precise research insights across diverse asset classes, including equities and crypto.

**PROFESSIONAL EXPERIENCE**
Washington University in St. Louis, Olin Business School	St. Louis, MO, USA
Research Assistant	May 2024 - Present
Overview: Data scientist in processing novel databases, fine-tuning sentiment analysis models, and AI-LLM market forecasting
-	Developed a Selenium web scraper to extract data from social media and news databases, improved sentiment classification through BERT model fine-tuning, transforming it into a key resource for quantitative research
-	Cleansed a novel, century-long, 400,000-entry United States' congressional hearing database for market insights
-	Drafted a Stata pipeline for processing confidential SEC data, facilitating efficient handling of large-scale confidential dataset
Privium Fund Management	Hong Kong
Portfolio Manager	Apr 2022 - Dec 2022
Overview: Co-managed US$ 200M AUM options selling strategy, overseeing algorithmic trading and risk management
-	Executed options selling strategy on index options, minimizing slippage and maximizing premiums with algorithmic trading
-	Utilized risk analysis models to optimize portfolio management, performing sensitivity analysis on Greeks (Delta, Gamma, Vega, Theta) to ensure compliance with risk management standards
-	Applied GARCH models to assess potential volatility in target investments, supporting strategic decision-making
-	Managed liquidity and order book dynamics to reduce slippage and optimize risk-adjusted returns
-	Performed portfolio stress testing under various market scenarios to ensure robustness across $200M in managed assets
Yong Rong Asset	Hong Kong
Junior Trader	Jun 2021 - Jan 2022
Overview: Research-focused buy-side trader at a fundamental high-conviction macro sub-fund
-	Participated in trading activities for a high-conviction sub-fund with an AUM of $30M, focused on high-growth technology companies in North American equity markets. Maintained the firm's trading and reporting scripts to support execution
-	Produced comprehensive research memos, conducted detailed risk profile analysis in research reports, evaluating market volatility, financial stability, and operational risks, enabling accurate identification of risks in target investments 
Peak Global Investments	Hong Kong
Private Equity Intern	Sep 2020 - May 2021
Overview: Research, due diligence-focused intern while contributing to the firm's crypto and DeFi proprietary trading strategies
-	Researched cryptocurrency exchanges across Asia and Europe, liaised with senior executives to prepare for acquisitions
-	Conducted scenario analysis, modeling financial impacts under volatile market conditions to ensure resilience

**EDUCATION**
Washington University in St. Louis (WashU)	St. Louis, MO, USA
M.S. in Finance, Quantitative	Sep 2023 - Dec 2024 (Expected)
-	GPA: 3.95/4.00, Rank 2/80
-	Honors: All-semester Dean's List, Beta Gamma Sigma Award, Charles F. Knight Scholar (Expected)
-	Coursework: Quantitative Risk Management, Fixed Income Derivatives, Data Analysis Forecasting & Risk Analysis
The University of Hong Kong (HKU)	Hong Kong
B.S. in Economics and Finance	Sep 2017 - May 2021
-	GPA: 3.45/4.00, Rank 35%
-	Admitted based on achieving a top 0.4% province-ranking (143rd / 411,897) in National College Entrance Exam (Gaokao)
Institut d'Études Politiques de Paris (Sciences Po)	Paris, France
Scholarship-Awarded Exchange Student	Jan 2020 - May 2020
-	GPA: 17/20, Awarded HKU Reaching Out Award (C.V. Starr Scholarship)

**LEADERSHIP & ACTIVITIES**
Teaching	TA for: Options, Futures and Derivative Securities (Undergraduate); Behavioral Finance (Graduate)
Research	Data Matching for PEVC-backed Companies - Cornell University RA under Prof. Minmo Gahng; 
The Causal Impact of Fiscal Shocks - WashU RA under Prof. William Cassidy
Volunteering	NGO Marketing Director, Soap Cycling HKU; Volunteer Teacher, Beyond the Pivot HKU;
Organizations	Director of Public Relations, XGravity Outdoors Club HKU

**SKILLS & PERSONAL**
Certificates	CFA Level II Candidate, FRM Level I Candidate, HKSFC Type-9 Asset Management License
Technical	Python, R, Stata, SQL, Git, MATLAB, VBA, LaTeX, Bloomberg, Capital IQ, Microsoft Office, Tableau
Languages	Mandarin (Native), English (Fluent, IELTS 8.0), Cantonese (Intermediate)
Work Permits	Hong Kong SAR (Nationality), Canada (OWP with Citizenship Assurance), USA (OPT)
"""


def get_cv(cv_type):
    if cv_type == "trader_quant_data":
        return cv_trader_quant_data
    elif cv_type == "research":
        return cv_research
    elif cv_type == "equity_research":
        return cv_equity_research
    elif cv_type == "pan_finance":
        return cv_pan_finance
    elif cv_type == "ibd":
        return cv_ibd
    elif cv_type == "operation":
        return cv_operation
    elif cv_type == "risk":
        return cv_risk
    else:
        return cv_trader_quant_data


def cv_location(cv_folder, cv_type):
    if cv_type == "trader_quant_data":
        return f"{cv_folder}/trader.pdf"
    elif cv_type == "research":
        return f"{cv_folder}/research.pdf"
    elif cv_type == "equity_research":
        return f"{cv_folder}/equity research.pdf"
    elif cv_type == "pan_finance":
        return f"{cv_folder}/pan-finance.pdf"
    elif cv_type == "ibd":
        return f"{cv_folder}/ibd.pdf"
    elif cv_type == "operation":
        return f"{cv_folder}/operation.pdf"
    elif cv_type == "risk":
        return f"{cv_folder}/risk.pdf"
    else:
        return f"{cv_folder}/trader.pdf"


def get_professional_summary(cv):

    # Extract the professional summary section from the CV
    prof_summary = re.search(
        r"(PROFESSIONAL SUMMARY|SUMMARY)(.*?)(PROFESSIONAL|EXPERIENCE)", cv, re.DOTALL)
    if prof_summary:
        return prof_summary.group(2).replace("**", "").strip()
    else:
        return None


def help_me_choose_cv(
    jd_required,
    cv_i_chose,
    cv_trader_quant_data=cv_trader_quant_data,
    cv_research=cv_research,
    cv_equity_research=cv_equity_research,
    cv_pan_finance=cv_pan_finance,
    cv_ibd=cv_ibd,
    cv_operation=cv_operation,
    cv_risk=cv_risk,
):
    import re
    from gpt_functions import chatgpt

    jd_clean = jd_required.replace("\n", " ")
    system_msg = f"""You are a helpful assistant helping a job seeker choose the best CV version to apply for a job. The job description goes as follows: {jd_clean}"""
    query = f"""**Return me with **version name** of the most suitable CV to use based on each version of my CV's professional summary section, no need to tell me CV content or state any reasons.
**Version name: "trader_quant_data":**
{get_professional_summary(cv_trader_quant_data)}

**Version name: "research":**
{get_professional_summary(cv_research)}

**Version name: "equity_research":**
{get_professional_summary(cv_equity_research)}

**Version name: "pan_finance":**
{get_professional_summary(cv_pan_finance)}

**Version name:"ibd":**
{get_professional_summary(cv_ibd)}

**Version name: "operation":**
{get_professional_summary(cv_operation)}

**Version name: "risk":**
{get_professional_summary(cv_risk)}"""

    model = "gpt-4o-mini"
    retry_max = 5
    retry = 0
    valid_versions = {
        "trader_quant_data",
        "research",
        "equity_research",
        "pan_finance",
        "ibd",
        "operation",
        "risk",
    }

    while retry < retry_max:
        try:
            answer = chatgpt(model, query, system_msg=system_msg)
            if answer:
                answer_clean = (
                    answer.lower().replace("version", "").replace("name", "").strip()
                )
                answer_clean = re.sub(r"[^\w\s]", "", answer_clean).strip()

                if answer_clean in valid_versions:
                    if not cv_i_chose == "undecided":
                        new_prompt = f"""You chose version "{answer_clean} while my previous choice was "{cv_i_chose}. I am not saying that my choice is more superior and well-rounded, but can you please tell me your reasoning for choosing {answer_clean} within two sentences? If you changed your mind, please also let me know. Thank you!"""
                    else:
                        new_prompt = f"""You chose version "{answer_clean}. Please tell me your reasoning for choosing this version within two sentences. Thank you!"""

                    reason = chatgpt(
                        model=model,
                        prompt=new_prompt,
                        system_msg=system_msg,
                        last_prompt=query,
                        last_answer=answer,
                    )
                    return answer_clean, reason
            retry += 1
        except Exception as e:
            print(f"Error during chatgpt call: {e}")
            retry += 1

    # If no valid answer is found after retries
    print("Unable to determine the most suitable CV version.")
    return answer_clean, None
