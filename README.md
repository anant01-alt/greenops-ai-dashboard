## Hurdle 3 – Concept Check

### What is RMSE and what does a lower value indicate?

RMSE (Root Mean Squared Error) measures the average prediction error of a model. A lower RMSE indicates that predictions are closer to the actual values and the model is performing better.

### Why do we create lag features for time-series prediction instead of using the date directly?

Lag features allow the model to learn patterns from previous observations. Historical values are often more informative for forecasting than the date itself.

### What are the risks of using Linear Regression for this task? What assumptions does it make?

Linear Regression assumes a linear relationship between features and the target variable. It may struggle with nonlinear trends, seasonality, and sudden changes in cloud usage patterns. More advanced models can capture these patterns better.