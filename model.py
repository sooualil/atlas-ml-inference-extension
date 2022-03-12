import os
from pickle import load
from typing import Any, Dict, List
from pandas import DataFrame

from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.tree import ExtraTreeClassifier


class Model:
    columns: List[str]
    columns_to_encode: List[str]
    columns_encoder: Dict[str, LabelEncoder]
    label_encoder: LabelEncoder 
    features_scaler: MinMaxScaler
    model: ExtraTreeClassifier
    def __init__(self, path):
        pickles = ['columns.p', 'columns_encode.p', 'columns_encoder.p', 'le_encoder.p', 'scaler.p', 'model.p']
        self.columns, self.columns_to_encode, self.columns_encoder, self.label_encoder, self.features_scaler, self.model =\
            (load(open(os.path.join(path, p), 'rb')) for p in pickles)

    def preprocess_df(self, test: Dict[str, List]):
        """
        This function preprocess the raw data, performing columns selection, encoding and features scalung
        """
        df_test = DataFrame(test)
        df_test = df_test[self.columns]
        for col in self.columns_to_encode:
            df_test[col] = df_test[col].str.strip()
            df_test[col] = self.columns_encoder[col].transform(df_test[col])
        X_test = self.features_scaler.transform(df_test)
        return X_test

    def predict(self, test):
        X_test = self.preprocess_df(test)
        predictions = self.model.predict(X_test)
        predicted_labels = self.label_encoder.inverse_transform(predictions)
        return predictions, predicted_labels

    
