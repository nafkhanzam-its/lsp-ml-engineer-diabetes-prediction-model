#!/usr/bin/env python3
"""
Diabetes Risk Prediction System
Klinik Sehat Sentosa

Script untuk prediksi risiko diabetes menggunakan model machine learning
yang telah dilatih pada data rekam medis pasien.

Usage:
    python diabetes_predictor.py --interactive
    python diabetes_predictor.py --batch input.csv
"""

import numpy as np
import pandas as pd
import joblib
import argparse
import json
from datetime import datetime
import os
import sys

class DiabetesPredictor:
    """
    Kelas untuk prediksi risiko diabetes menggunakan model yang telah dilatih
    """

    def __init__(self, model_path=None, scaler_path=None):
        """
        Inisialisasi predictor

        Args:
            model_path (str): Path ke file model (.pkl)
            scaler_path (str): Path ke file scaler (.pkl)
        """
        self.model = None
        self.scaler = None
        self.feature_names = [
            'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
            'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
        ]

        if model_path and scaler_path:
            self.load_model(model_path, scaler_path)

    def load_model(self, model_path, scaler_path):
        """
        Load model dan scaler yang telah disimpan

        Args:
            model_path (str): Path ke file model
            scaler_path (str): Path ke file scaler
        """
        try:
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            print(f"✓ Model berhasil dimuat dari: {model_path}")
            print(f"✓ Scaler berhasil dimuat dari: {scaler_path}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            sys.exit(1)

    def validate_input(self, data):
        """
        Validasi input data medis

        Args:
            data (dict): Dictionary dengan data pasien

        Returns:
            bool: True jika valid, False jika tidak
        """
        required_fields = self.feature_names

        # Cek kelengkapan field
        for field in required_fields:
            if field not in data:
                print(f"❌ Field '{field}' tidak ditemukan")
                return False

        # Validasi range nilai
        validations = {
            'Pregnancies': (0, 20),
            'Glucose': (50, 300),
            'BloodPressure': (40, 200),
            'SkinThickness': (0, 100),
            'Insulin': (0, 900),
            'BMI': (10, 60),
            'DiabetesPedigreeFunction': (0, 3),
            'Age': (10, 120)
        }

        for field, (min_val, max_val) in validations.items():
            value = data[field]
            if not isinstance(value, (int, float)) or not (min_val <= value <= max_val):
                print(f"❌ Nilai '{field}' tidak valid: {value} (harus {min_val}-{max_val})")
                return False

        return True

    def predict_single(self, patient_data):
        """
        Prediksi untuk satu pasien

        Args:
            patient_data (dict): Data pasien

        Returns:
            dict: Hasil prediksi dengan probabilitas dan kategori risiko
        """
        if not self.validate_input(patient_data):
            return None

        # Siapkan data input
        input_array = np.array([[
            patient_data['Pregnancies'],
            patient_data['Glucose'],
            patient_data['BloodPressure'],
            patient_data['SkinThickness'],
            patient_data['Insulin'],
            patient_data['BMI'],
            patient_data['DiabetesPedigreeFunction'],
            patient_data['Age']
        ]])

        # Prediksi dengan atau tanpa scaling tergantung model
        model_name = type(self.model).__name__
        if model_name in ['LogisticRegression', 'SVC']:
            input_scaled = self.scaler.transform(input_array)
            prediction = self.model.predict(input_scaled)[0]
            probability = self.model.predict_proba(input_scaled)[0][1]
        else:
            prediction = self.model.predict(input_array)[0]
            probability = self.model.predict_proba(input_array)[0][1]

        # Kategorisasi risiko
        if probability < 0.3:
            risk_category = "Low Risk"
            risk_color = "🟢"
        elif probability < 0.7:
            risk_category = "Medium Risk"
            risk_color = "🟡"
        else:
            risk_category = "High Risk"
            risk_color = "🔴"

        # Rekomendasi berdasarkan risiko
        recommendations = self._get_recommendations(risk_category, patient_data)

        return {
            'prediction': int(prediction),
            'prediction_label': 'Diabetes' if prediction == 1 else 'No Diabetes',
            'probability': float(probability),
            'probability_percent': f"{probability * 100:.1f}%",
            'risk_category': risk_category,
            'risk_color': risk_color,
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        }

    def _get_recommendations(self, risk_category, patient_data):
        """
        Generate rekomendasi berdasarkan kategori risiko dan data pasien
        """
        base_recommendations = [
            "Maintain healthy diet with balanced nutrition",
            "Regular physical exercise (150 minutes/week)",
            "Monitor blood glucose regularly",
            "Maintain healthy weight"
        ]

        if risk_category == "High Risk":
            return base_recommendations + [
                "⚠️ Immediate consultation with endocrinologist recommended",
                "Consider HbA1c and oral glucose tolerance test",
                "Strict diet modification and lifestyle changes",
                "Monthly follow-up appointments"
            ]
        elif risk_category == "Medium Risk":
            return base_recommendations + [
                "Schedule follow-up in 3-6 months",
                "Consider dietary consultation",
                "Increase physical activity intensity",
                "Monitor BMI and blood pressure"
            ]
        else:
            return base_recommendations + [
                "Continue healthy lifestyle",
                "Annual screening recommended",
                "Maintain current health status"
            ]

    def predict_batch(self, csv_path, output_path=None):
        """
        Prediksi untuk multiple pasien dari file CSV

        Args:
            csv_path (str): Path ke file CSV input
            output_path (str): Path untuk menyimpan hasil (optional)
        """
        try:
            df = pd.read_csv(csv_path)
            print(f"📊 Processing {len(df)} patients...")

            results = []
            for idx, row in df.iterrows():
                patient_data = row.to_dict()
                result = self.predict_single(patient_data)
                if result:
                    result['patient_id'] = idx + 1
                    results.append(result)

            # Simpan hasil
            if output_path:
                # Create output directory if it doesn't exist
                output_dir = os.path.dirname(output_path)
                if output_dir and not os.path.exists(output_dir):
                    os.makedirs(output_dir, exist_ok=True)

                output_df = pd.DataFrame(results)
                output_df.to_csv(output_path, index=False)
                print(f"✓ Results saved to: {output_path}")

            # Summary
            high_risk = sum(1 for r in results if r['risk_category'] == 'High Risk')
            medium_risk = sum(1 for r in results if r['risk_category'] == 'Medium Risk')
            low_risk = sum(1 for r in results if r['risk_category'] == 'Low Risk')

            print(f"\n📈 RISK DISTRIBUTION:")
            print(f"🔴 High Risk: {high_risk} patients ({high_risk/len(results)*100:.1f}%)")
            print(f"🟡 Medium Risk: {medium_risk} patients ({medium_risk/len(results)*100:.1f}%)")
            print(f"🟢 Low Risk: {low_risk} patients ({low_risk/len(results)*100:.1f}%)")

            return results

        except Exception as e:
            print(f"❌ Error processing batch: {e}")
            return None

def interactive_mode(predictor):
    """
    Mode interaktif untuk input manual data pasien
    """
    print("\n" + "="*60)
    print("🏥 DIABETES RISK PREDICTION SYSTEM")
    print("   Klinik Sehat Sentosa")
    print("="*60)

    while True:
        print("\n📝 Input Data Pasien:")

        try:
            patient_data = {}

            # Input data dengan validasi
            patient_data['Pregnancies'] = int(input("Jumlah kehamilan: "))
            patient_data['Glucose'] = float(input("Glucose level (mg/dL): "))
            patient_data['BloodPressure'] = float(input("Blood pressure (mmHg): "))
            patient_data['SkinThickness'] = float(input("Skin thickness (mm): "))
            patient_data['Insulin'] = float(input("Insulin level (mu U/ml): "))
            patient_data['BMI'] = float(input("BMI: "))
            patient_data['DiabetesPedigreeFunction'] = float(input("Diabetes pedigree function: "))
            patient_data['Age'] = int(input("Age (years): "))

            # Prediksi
            print("\n🔄 Processing...")
            result = predictor.predict_single(patient_data)

            if result:
                print(f"\n{result['risk_color']} HASIL PREDIKSI {result['risk_color']}")
                print(f"Prediksi: {result['prediction_label']}")
                print(f"Probabilitas: {result['probability_percent']}")
                print(f"Kategori Risiko: {result['risk_category']}")

                print(f"\n💡 REKOMENDASI:")
                for i, rec in enumerate(result['recommendations'], 1):
                    print(f"  {i}. {rec}")

                # Simpan hasil jika diinginkan
                save = input(f"\nSimpan hasil ke file? (y/n): ").lower().strip()
                if save == 'y':
                    # Create output directory if it doesn't exist
                    os.makedirs('output/predictions', exist_ok=True)

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"output/predictions/diabetes_prediction_{timestamp}.json"
                    with open(filename, 'w') as f:
                        json.dump(result, f, indent=2)
                    print(f"✓ Hasil disimpan ke: {filename}")

        except ValueError as e:
            print(f"❌ Input tidak valid: {e}")
        except KeyboardInterrupt:
            print(f"\n\n👋 Program dihentikan. Terima kasih!")
            break

        # Lanjut atau keluar
        continue_pred = input(f"\nPrediksi pasien lain? (y/n): ").lower().strip()
        if continue_pred != 'y':
            print(f"👋 Terima kasih telah menggunakan sistem prediksi diabetes!")
            break

def main():
    parser = argparse.ArgumentParser(description='Diabetes Risk Prediction System')
    parser.add_argument('--interactive', action='store_true',
                       help='Run in interactive mode for single patient prediction')
    parser.add_argument('--batch', type=str,
                       help='Path to CSV file for batch prediction')
    parser.add_argument('--output', type=str,
                       help='Output path for batch prediction results')
    parser.add_argument('--model', type=str,
                       help='Path to model file (.pkl)')
    parser.add_argument('--scaler', type=str,
                       help='Path to scaler file (.pkl)')

    args = parser.parse_args()

    # Auto-detect model files jika tidak dispesifikasi
    model_files = [f for f in os.listdir('.') if f.startswith('diabetes_prediction_model_') and f.endswith('.pkl')]
    scaler_file = 'diabetes_scaler.pkl'

    if args.model and args.scaler:
        model_path = args.model
        scaler_path = args.scaler
    elif model_files and os.path.exists(scaler_file):
        model_path = model_files[0]  # Ambil model pertama yang ditemukan
        scaler_path = scaler_file
        print(f"🔍 Auto-detected model: {model_path}")
        print(f"🔍 Auto-detected scaler: {scaler_path}")
    else:
        print("❌ Model atau scaler tidak ditemukan!")
        print("Pastikan file model (.pkl) dan scaler (diabetes_scaler.pkl) ada di direktori yang sama.")
        sys.exit(1)

    # Inisialisasi predictor
    predictor = DiabetesPredictor(model_path, scaler_path)

    if args.interactive:
        interactive_mode(predictor)
    elif args.batch:
        output_path = args.output or f"output/batch/batch_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        predictor.predict_batch(args.batch, output_path)
    else:
        # Default ke interactive mode jika tidak ada argument
        interactive_mode(predictor)

if __name__ == "__main__":
    main()