Based on the CSV file in this folder, act like a fraud risk analyst reviewing a queue of loan applications.

Your job is to identify the most suspicious cases, explain the fraud signals clearly, connect any linked patterns across cases, and generate concise outputs that help a fraud team decide what to review first.

Please do all of the following in one response:

## 1) Executive summary
Write a short summary of what stands out in this dataset:
- how many cases look low, medium, and high risk
- what the biggest suspicious patterns are
- whether there are signs of coordinated activity, synthetic identity risk, or first-party fraud

## 2) Ranked review queue
Create a table ranking the top 5 cases that should be reviewed first.

Include these columns:
- case_id
- review_priority
- fraud_label
- key_signals
- why_it_matters
- recommended_next_step

Keep the explanations short and practical.

## 3) Linked-pattern analysis
Look across all cases and identify any shared fraud patterns, such as:
- repeated device_id
- repeated ip_address
- suspiciously similar employer names
- similar email naming conventions
- income mismatches
- recently opened bank accounts
- any clusters that may indicate coordinated activity

Create a table:
Pattern | Related Cases | Why It Matters | Suggested Action

## 4) Visuals and figures
Generate simple outputs that would help someone understand the fraud risk quickly, such as:
- a fraud risk summary table
- a bar chart of cases by review priority
- a chart or table showing linked cases by shared device or IP
- any other visual that helps explain the suspicious patterns

## 5) Investigation memo
Write a short investigation memo for the most suspicious cases:
- one paragraph summary
- bullet list of evidence
- risk assessment
- recommended disposition
- what should be verified next

## 6) Evidence appendix
Create a compact evidence appendix showing, for each top suspicious case:
- case_id
- main suspicious fields
- exact values from the CSV that drove concern
- a short explanation of why those values are suspicious

Keep the tone professional, clear, and useful for a real fraud operations team. Focus on explainability, not just scoring.