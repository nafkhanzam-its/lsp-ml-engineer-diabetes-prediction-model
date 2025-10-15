#!/usr/bin/env python3
"""
Diabetes Risk Prediction Web Application
Klinik Sehat Sentosa

Flask web application for diabetes risk prediction with modern UI
"""

from flask import Flask, render_template, request, jsonify, flash
import os
from datetime import datetime
from diabetes_predictor import DiabetesPredictor

app = Flask(__name__)
app.secret_key = 'diabetes_prediction_secret_key_2024'

# Global predictor instance
predictor = None

def initialize_predictor():
    """Initialize the diabetes predictor with auto-detected models"""
    global predictor

    # Auto-detect model files in current directory or models folder
    model_files = []
    scaler_file = None

    # Check current directory first
    if os.path.exists('.'):
        model_files = [f for f in os.listdir('.') if f.startswith('diabetes_prediction_model_') and f.endswith('.pkl')]
        if os.path.exists('diabetes_scaler.pkl'):
            scaler_file = 'diabetes_scaler.pkl'

    # Check models directory if not found in current directory
    if not model_files and os.path.exists('models'):
        model_files = [os.path.join('models', f) for f in os.listdir('models')
                      if f.startswith('diabetes_prediction_model_') and f.endswith('.pkl')]
        if os.path.exists('models/diabetes_scaler.pkl'):
            scaler_file = 'models/diabetes_scaler.pkl'

    if model_files and scaler_file:
        model_path = model_files[0]
        scaler_path = scaler_file
        predictor = DiabetesPredictor(model_path, scaler_path)
        print(f"✓ Model loaded: {model_path}")
        return True
    else:
        print("❌ Model files not found!")
        return False

@app.route('/')
def index():
    """Main page with prediction form"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page with project information"""
    return render_template('about.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction request via AJAX"""
    try:
        # Get form data
        data = request.get_json()

        # Validate required fields
        required_fields = ['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness',
                          'insulin', 'bmi', 'diabetes_pedigree', 'age']

        patient_data = {}
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400

            try:
                patient_data[field.replace('_', '').title() if field != 'bmi' else 'BMI'] = float(data[field])
            except ValueError:
                return jsonify({'error': f'Invalid value for {field}'}), 400

        # Map to correct field names
        prediction_data = {
            'Pregnancies': patient_data['Pregnancies'],
            'Glucose': patient_data['Glucose'],
            'BloodPressure': patient_data['Bloodpressure'],
            'SkinThickness': patient_data['Skinthickness'],
            'Insulin': patient_data['Insulin'],
            'BMI': patient_data['BMI'],
            'DiabetesPedigreeFunction': patient_data['Diabetespedigree'],
            'Age': patient_data['Age']
        }

        # Make prediction
        result = predictor.predict_single(prediction_data)

        if result is None:
            return jsonify({'error': 'Invalid input data'}), 400

        # Format response
        response = {
            'success': True,
            'prediction': result['prediction_label'],
            'probability': result['probability_percent'],
            'risk_category': result['risk_category'],
            'risk_color': result['risk_color'],
            'recommendations': result['recommendations'],
            'timestamp': result['timestamp']
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for deployment"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': predictor is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/stats')
def get_stats():
    """Get some basic statistics about the model"""
    if predictor is None:
        return jsonify({'error': 'Model not loaded'}), 500

    # Read some basic info (this would be from a database in production)
    stats = {
        'total_predictions': 0,  # Would come from database
        'high_risk_detected': 0,  # Would come from database
        'model_accuracy': '85.2%',  # From model evaluation
        'last_updated': '2024-10-15'
    }

    return jsonify(stats)

if __name__ == '__main__':
    # Initialize predictor
    if initialize_predictor():
        print("🚀 Starting Diabetes Prediction Web Application...")
        print("📱 Access the application at: http://localhost:5000")
        print("🛑 Press Ctrl+C to stop the server")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Failed to initialize predictor. Please ensure model files are present.")
        print("💡 Make sure these files exist:")
        print("   - diabetes_prediction_model_*.pkl")
        print("   - diabetes_scaler.pkl")