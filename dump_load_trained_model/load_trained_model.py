from joblib import load

model = load('model_joblib')
print(f'Coefficient : {model.coef_}')
print(f'Intercept : {model.intercept_}')

print(model.predict([[5000]]))