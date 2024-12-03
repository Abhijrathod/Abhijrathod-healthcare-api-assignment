# **Backend  Assignment: BE (Intern)**

This project is a Django REST API for managing and analyzing blood test results. It is designed to demonstrate technical proficiency, code hygiene, and a creative approach to problem-solving.

---

## **The Goal**

To create a scalable and efficient API that processes and analyzes sample medical test results while adhering to best practices in API development.

---

## **Features**

### Core Features:
1. **Store Blood Test Records**:
   - `patient_id`: Unique identifier for the patient.
   - `test_name`: Type of test (e.g., `GLUCOSE`, `HB`, `CHOL`).
   - `value`: Measured value of the test.
   - `unit`: Unit of measurement.
   - `test_date`: Date and time of the test.
   - `is_abnormal`: Boolean indicating if the result is abnormal.

2. **API Endpoints**:
   - **POST** `/api/tests/`: Create a new test record.
   - **GET** `/api/tests/?patient_id=123`: Retrieve all test results for a specific patient.
   - **GET** `/api/tests/stats/`: Retrieve basic statistics for each test type (min, max, average, abnormal counts).

3. **Advanced Feature**:
   - Implemented **batch upload of test results via CSV** to simplify bulk data ingestion.

---

## **Technical Implementation**

### **Model**

The `TestResult` model is used to store blood test data:
```python
class TestResult(models.Model):
    patient_id = models.IntegerField(validators=[MinValueValidator(1)])
    test_name = models.CharField(
        max_length=100,
        choices=[
            ('GLUCOSE', 'Blood Glucose'),
            ('HB', 'Hemoglobin'),
            ('CHOL', 'Cholesterol')
        ]
    )
    value = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=10)
    test_date = models.DateTimeField()
    is_abnormal = models.BooleanField()

    class Meta:
        indexes = [
            models.Index(fields=['patient_id', 'test_name'])
        ]
