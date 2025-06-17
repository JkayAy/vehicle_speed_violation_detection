# Model Card: YOLOv8 for Vehicle Detection

## Model Details
- **Architecture**: YOLOv8
- **Task**: Vehicle detection in video frames
- **Input**: Video frames (RGB images)
- **Output**: Bounding boxes for detected vehicles

## Intended Use
- Detect vehicles in traffic camera feeds or uploaded videos
- Calculate vehicle speed and identify speed violations

## Limitations
- Performance may degrade in poor lighting or weather conditions
- May not generalize to all vehicle types or regions
- OCR accuracy depends on license plate clarity

## Ethical Considerations
- Should not be used for surveillance without proper authorization
- May inherit biases from training data
- Users should ensure compliance with local laws and privacy regulations

## Training Data
- Trained on public vehicle datasets (details in training script)

## Metrics
- mAP, precision, recall (see training logs)

## Contact
- For questions, contact [your-email@example.com] 