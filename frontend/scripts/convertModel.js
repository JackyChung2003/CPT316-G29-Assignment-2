import * as tf from '@tensorflow/tfjs-node'; // Use the Node.js version of TensorFlow.js
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Paths for the Keras model and the output directory
const kerasModelPath = path.resolve(__dirname, '../../backend/models/toxic_comment_cnn.h5');
const outputDir = path.resolve(__dirname, '../../backend/models/tfjs_model');

async function convertModel() {
  try {
    // Load the Keras model
    const model = await tf.loadLayersModel(`file://${kerasModelPath}`);

    // Save the model in TensorFlow.js format
    await model.save(`file://${outputDir}`);
    console.log('Model converted successfully!');
  } catch (error) {
    console.error('Error converting the model:', error.message);
  }
}

convertModel();
