# PSEG PDF Parser

A nifty little helper script to turn pseg pdfs into csvs. Requires PSEG exports in PDF format to be downloaded into a local folder called 'bills'.

I keep track of all my bills because I'm a nerd. A responsible nerd.
Tracking energy usage is tedious because my energy company only provides bills in PDF format. No API, and the CSV export takes forever (and possibly doesn't even work). There are companies like utilityapi that look like fun to use, but you have to pay to play. I haven't written anything new in quite some time, and I've been wanting to do just that for a while now.

My personal budget doc has a worksheet containing historical energy cost data. This helper script will take a PSEG bill in PDF form and output a new row.

|Start Period|End Period| Electric Charges | Gas Charges | Amount Due |Usage (kWh)| Delivery Rate ($/kWh) | Delivery Charges (Electric) | Supply Rate ($/kWh) |Supply Charges (Electric)|Usage (Therms)| Delivery Rate ($/Therm) | Delivery Charges (Gas) | Supply Rate ($/Therm) | Supply Charges (Gas) | Rolling 3-Month Avg |Electric YoY|Gas YoY|Total YoY|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|1/6/22|2/3/22| $95.44 | $110.68 | $206.12 |551| $0.04 | $29.29 | $0.12 | $66.15 |116.752| $0.42 | $67.74 | $0.37 | $42.94 | $163.65 |-35%|1081%|32%|
|2/4/22|3/7/22| $81.85 | $83.86 | $165.71 |482| $0.04 | $26.22 | $0.11 | $55.63 |82.476| $0.42 | $50.03 | $0.41 | $33.83 | $174.70 |-35%|795%|22%|
|3/8/22|4/5/22| $70.05 | $56.23 | $126.28 |370| $0.04 | $21.28 | $0.13 | $48.77 |52.485| $0.42 | $34.70 | $0.41 | $21.53 | $166.04 |-6%|552%|52%|
|4/6/22|5/5/22| $63.66 | $34.44 | $98.10 |326| $0.04 | $19.34 | $0.14 | $44.32 |28.92| $0.42 | $22.57 | $0.41 | $11.87 | $130.03 |16%|300%|54%|
|5/6/22|6/6/22| $111.50 | $19.35 | $130.85 |570| $0.05 | $34.44 | $0.14 | $77.06 |12.841| $0.42 | $14.08 | $0.41 | $5.27 | $118.41 |-15%|-36%|-19%|
|6/7/22|7/6/22| $147.92 | $19.62 | $167.54 |757| $0.05 | $46.49 | $0.13 | $101.43 |12.816| $0.43 | $14.36 | $0.41 | $5.26 | $132.16 |-14%|22%|-11%|
|7/7/22|8/3/22| $160.39 | $17.81 | $178.20 |819| $0.05 | $50.18 | $0.13 | $110.21 |10.66| $0.45 | $13.44 | $0.41 | $4.37 | $158.86 |15%|22%|15%|
|8/4/22|9/2/22| $170.63 | $19.66 | $190.29 |876| $0.05 | $53.49 | $0.13 | $117.14 |12.804| $0.45 | $14.41 | $0.41 | $5.25 | $178.68 |15%|28%|16%|
|9/3/22|10/4/22| $102.88 | $25.54 | $128.42 |620| $0.04 | $32.64 | $0.11 | $70.24 |18.156| $0.45 | $17.32 | $0.45 | $8.22 | $165.64 |20%|64%|27%|
|10/5/22|11/2/22| $76.55 | $41.52 | $118.07 |444| $0.05 | $25.09 | $0.12 | $51.46 |27.768| $0.48 | $23.42 | $0.65 | $18.10 | $145.59 |15%|128%|40%|
|11/3/22|12/5/22| $132.28 | $85.23 | $217.51 |777| $0.05 | $40.19 | $0.12 | $92.09 |63.379| $0.48 | $43.92 | $0.65 | $41.31 | $154.67 |61%|69%|64%|
|12/6/22|1/5/23| $160.95 | $106.57 | $267.52 |874| $0.05 | $44.59 | $0.13 | $116.36 |80.024| $0.49 | $54.41 | $0.65 | $52.16 | $201.03 |103%|46%|76%|

