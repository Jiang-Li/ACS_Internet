# Understanding PERWT in ACS Data Analysis

## What is PERWT and Why Does It Matter?

PERWT, or Person Weight, is a value given to each person in the American Community Survey (ACS) personal-level data. It shows how many people in the U.S. population that individual represents. This matters because the ACS is a sample survey—not a complete count of everyone in the country. Without weights, your results might only show patterns in the sample, which could be skewed depending on who was included or left out. PERWT helps fix this by scaling each person's data to match the real population.

## How to Use PERWT in Calculations

To use PERWT, you calculate weighted statistics to reflect the population accurately:

- **For Averages**: Multiply each person's value (like income) by their PERWT, add up all these products, and then divide by the total sum of PERWTs for the group you're studying.

- **For Proportions**: To find a percentage (like the share of people using the internet), sum the PERWTs for those who meet your condition (e.g., internet users) and divide by the total sum of PERWTs for the group.

The logic is simple: PERWT ensures each person's contribution matches their real-world representation, not just their presence in the sample.

## Practical Examples

### Example 1: Average Income by State

Imagine you want to find the average income in Texas using ACS data:

1. Filter your data to only include people from Texas (using a state identifier like STATEFIP = 48).

2. For each person, multiply their income (from a variable like PINCP) by their PERWT:
   ```
   Person A: Income = $40,000, PERWT = 60 → $40,000 × 60 = $2,400,000
   Person B: Income = $55,000, PERWT = 45 → $55,000 × 45 = $2,475,000
   Person C: Income = $30,000, PERWT = 50 → $30,000 × 50 = $1,500,000
   ```

3. Add these up: $2,400,000 + $2,475,000 + $1,500,000 = $6,375,000.

4. Sum the PERWTs: 60 + 45 + 50 = 155.

5. Divide the total weighted income by the total PERWT: $6,375,000 ÷ 155 = $41,129.03.

**Result**: The average income in Texas, adjusted for the population, is about $41,129. Without weights, you'd just average $40,000, $55,000, and $30,000 (=$41,666), which might not reflect the true population due to sampling differences.

### Example 2: Internet Usage by Education Level

Now, let's estimate the proportion of college graduates who use the internet at home via a cellular data plan (using CINETHOMEMODE = 4, where 4 means "cellular data plan only"):

1. Filter the data to people with a college degree (e.g., EDUC = 6 for bachelor's degree or higher).

2. Identify who uses a cellular data plan for internet (CINETHOMEMODE = 4):
   ```
   Person A: CINETHOMEMODE = 4, PERWT = 50 (uses cellular data)
   Person B: CINETHOMEMODE = 1, PERWT = 45 (uses broadband, not cellular)
   Person C: CINETHOMEMODE = 4, PERWT = 60 (uses cellular data)
   Person D: CINETHOMEMODE = 3, PERWT = 55 (uses satellite, not cellular)
   ```

3. Sum the PERWTs for those with CINETHOMEMODE = 4: 50 + 60 = 110.

4. Sum all PERWTs for college graduates: 50 + 45 + 60 + 55 = 210.

5. Divide the weighted sum of internet users by the total: 110 ÷ 210 = 0.5238, or 52.38%.

**Result**: About 52.4% of college graduates rely on cellular data plans for internet at home. Without weights, you'd count 2 out of 4 people (50%), which might not match the population if the sample over- or under-represents certain groups.

## Why This Works

In the income example, Person B's higher income gets more influence because their PERWT (45) is substantial, but not as much as Person C's (50), balancing the sample to reflect the population. In the internet usage example, weights show that cellular data users represent a larger share of the population than their raw count suggests, giving a truer picture.

## An Unexpected Twist

One thing to note: in ACS data, "internet usage" like CINETHOMEMODE doesn't measure hours spent online or phone calls—it's about how people connect to the internet at home (e.g., cellular data, broadband, etc.). This might catch you off guard if you expected something like "average minutes on TikTok." It's a proxy for access, not direct usage, but it's still useful for understanding connectivity trends.

## Implementation in This Project

In our analysis script (`src/analysis/analyze_weighted_stats.py`), we use PERWT to calculate weighted percentages of internet and smartphone access. Here's a key function that implements this:

```python
def calculate_weighted_percentage(df, weight_col, condition_col, condition_value=1):
    """Calculate weighted percentage for a given condition."""
    total_weight = df[weight_col].sum()
    if total_weight == 0:
        return 0
    condition_weight = df[df[condition_col] == condition_value][weight_col].sum()
    return (condition_weight / total_weight * 100)
```

This function:
1. Takes a DataFrame with person-level data
2. Uses PERWT as the weight column
3. Calculates the weighted percentage of people meeting a specific condition
4. Returns the result as a percentage

For example, when calculating internet access by state, we:
1. Filter the data for each state
2. Use PERWT to weight each person's internet access status
3. Calculate the weighted percentage of people with internet access
4. Repeat for all states to get representative statistics 