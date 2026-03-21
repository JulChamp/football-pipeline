import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from xgboost import XGBClassifier

df = pd.read_csv("ml/dataset.csv")

FEATURES = [
    "home_wins_l5", "home_draws_l5", "home_losses_l5",
    "away_wins_l5", "away_draws_l5", "away_losses_l5"
]
X = df[FEATURES]
le = LabelEncoder()
y = le.fit_transform(df["target"])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.1)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=le.classes_))

# Sauvegarder le modèle
joblib.dump(model, "ml/model.joblib")
joblib.dump(le, "ml/label_encoder.joblib")
print("✅ Modèle sauvegardé")