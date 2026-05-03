import React, { useRef, useState, useCallback } from 'react';
import { Camera, RefreshCw, X, Check } from 'lucide-react';

interface FaceCaptureProps {
  onCapture: (imageBase64: string) => void;
  onClose: () => void;
  language: 'en' | 'my';
}

const FaceCapture: React.FC<FaceCaptureProps> = ({ onCapture, onClose, language }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [capturedImage, setCapturedImage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const startCamera = async () => {
    try {
      setError(null);
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: 'user', width: 640, height: 480 } 
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setIsCameraActive(true);
      }
    } catch (err) {
      console.error("Camera access error:", err);
      setError(language === 'my' ? "ကင်မရာ အသုံးပြုခွင့် မရှိပါ" : "Camera access denied");
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      stream.getTracks().forEach(track => track.stop());
      videoRef.current.srcObject = null;
      setIsCameraActive(false);
    }
  };

  const capturePhoto = useCallback(() => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const dataUrl = canvas.toDataURL('image/jpeg');
        setCapturedImage(dataUrl);
        stopCamera();
      }
    }
  }, []);

  const handleRetake = () => {
    setCapturedImage(null);
    startCamera();
  };

  const handleConfirm = () => {
    if (capturedImage) {
      onCapture(capturedImage);
    }
  };

  React.useEffect(() => {
    startCamera();
    return () => stopCamera();
  }, []);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
      <div className="bg-white dark:bg-gray-900 rounded-3xl overflow-hidden w-full max-w-md shadow-2xl border border-gray-200 dark:border-gray-800">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-100 dark:border-gray-800">
          <h3 className="text-lg font-bold text-gray-800 dark:text-white flex items-center gap-2">
            <Camera className="w-5 h-5 text-indigo-500" />
            {language === 'my' ? 'မျက်နှာဖြင့် Emotion စစ်ဆေးခြင်း' : 'Face Emotion Analysis'}
          </h3>
          <button 
            onClick={onClose}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full transition-colors"
          >
            <X className="w-5 h-5 text-gray-500" />
          </button>
        </div>

        {/* Camera/Preview Area */}
        <div className="relative aspect-video bg-black flex items-center justify-center">
          {error ? (
            <div className="text-center p-6">
              <p className="text-red-500 mb-4">{error}</p>
              <button 
                onClick={startCamera}
                className="px-4 py-2 bg-indigo-500 text-white rounded-xl font-medium"
              >
                {language === 'my' ? 'ပြန်ကြိုးစားပါ' : 'Retry'}
              </button>
            </div>
          ) : capturedImage ? (
            <img src={capturedImage} alt="Captured" className="w-full h-full object-cover" />
          ) : (
            <>
              <video 
                ref={videoRef} 
                autoPlay 
                playsInline 
                className="w-full h-full object-cover"
              />
              <div className="absolute bottom-4 left-0 right-0 flex justify-center">
                <button 
                  onClick={capturePhoto}
                  className="w-16 h-16 rounded-full bg-white/20 backdrop-blur-md border-4 border-white flex items-center justify-center hover:scale-105 active:scale-95 transition-all shadow-lg"
                >
                  <div className="w-12 h-12 rounded-full bg-white"></div>
                </button>
              </div>
            </>
          )}
          <canvas ref={canvasRef} className="hidden" />
        </div>

        {/* Footer Actions */}
        <div className="p-6 bg-gray-50 dark:bg-gray-900/50 flex justify-center gap-4">
          {capturedImage ? (
            <>
              <button
                onClick={handleRetake}
                className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-2xl font-semibold text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 transition-all shadow-sm"
              >
                <RefreshCw className="w-5 h-5" />
                {language === 'my' ? 'ပြန်ရိုက်မည်' : 'Retake'}
              </button>
              <button
                onClick={handleConfirm}
                className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-indigo-500 text-white rounded-2xl font-semibold hover:bg-indigo-600 transition-all shadow-lg shadow-indigo-500/25"
              >
                <Check className="w-5 h-5" />
                {language === 'my' ? 'စစ်ဆေးမည်' : 'Analyze'}
              </button>
            </>
          ) : (
            <p className="text-sm text-gray-500 dark:text-gray-400 text-center italic">
              {language === 'my' ? 'မျက်နှာကို ကင်မရာအလယ်တွင် ထားပေးပါ' : 'Center your face in the camera frame'}
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default FaceCapture;
