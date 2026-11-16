"""Rebuild missing LFS artifacts, separately from originals. Train-only fit, held-out test evaluation."""
import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from cognitive.perception import COLUMNS, CATEGORICAL, NUMERICAL, FEATURES

ROOT = Path(__file__).resolve().parents[1]


def rebuild():
    train = pd.read_csv(ROOT / 'data/KDDTrain+.txt', names=COLUMNS)
    test = pd.read_csv(ROOT / 'data/KDDTest+.txt', names=COLUMNS)
    xtrain, xtest = train[FEATURES].copy(), test[FEATURES].copy()
    encoders = {}
    for col in CATEGORICAL:
        encoder = LabelEncoder().fit(xtrain[col].astype(str))
        known = set(encoder.classes_)
        xtrain[col] = encoder.transform(xtrain[col].astype(str))
        xtest[col] = encoder.transform([x if x in known else encoder.classes_[0] for x in xtest[col].astype(str)])
        encoders[col] = encoder
    scaler = StandardScaler().fit(xtrain[NUMERICAL])
    xtrain[NUMERICAL] = scaler.transform(xtrain[NUMERICAL])
    xtest[NUMERICAL] = scaler.transform(xtest[NUMERICAL])
    ytrain = (train.label != 'normal').astype(int)
    ytest = (test.label != 'normal').astype(int)
    model = RandomForestClassifier(n_estimators=80, max_depth=22, min_samples_leaf=2,
                                   random_state=42, n_jobs=2, class_weight='balanced')
    model.fit(xtrain.astype(np.float32), ytrain)
    probs = model.predict_proba(xtest.astype(np.float32))[:, list(model.classes_).index(1)]
    pred = (probs >= .5).astype(int)
    output = ROOT / 'results/models/rebuilt'
    output.mkdir(parents=True, exist_ok=True)
    for name, obj in [('random_forest', model), ('scaler', scaler), ('label_encoders', encoders)]:
        joblib.dump(obj, output / f'{name}.pkl', compress=3)
    metrics = {'origin': 'Rebuilt locally because original artifacts are Git LFS pointers',
               'model': 'RandomForestClassifier (80 trees, depth 22, seed 42)',
               'training_rows': len(train), 'test_rows': len(test),
               'data': 'NSL-KDD train/test split; preprocessing fit on training only',
               'accuracy': accuracy_score(ytest, pred), 'precision': precision_score(ytest, pred),
               'recall': recall_score(ytest, pred), 'f1': f1_score(ytest, pred),
               'roc_auc': roc_auc_score(ytest, probs),
               'limitation': 'Historical offline data. These are legacy RF metrics, not DSS effectiveness.'}
    (output / 'metrics.json').write_text(json.dumps(metrics, indent=2), encoding='utf-8')
    print(json.dumps(metrics, indent=2))


if __name__ == '__main__':
    rebuild()
