#!/usr/bin/env python3
"""
单元测试：验证 audioboost 核心功能
- 测试音频文件加载/分析
- 测试波形处理逻辑
- 集成 FFmpeg 检查
"""

import unittest
import os
import tempfile
from audioboost.core import AudioAnalyzer  # 假设主模块名


class TestAudioCore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 生成一个测试用的静音音频文件（需要 ffmpeg）
        cls.test_audio = os.path.join(tempfile.gettempdir(), "test_silence.wav")
        os.system(f"ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t 1 {cls.test_audio}")

    def test_audio_metadata(self):
        """测试音频文件元数据读取"""
        analyzer = AudioAnalyzer(self.test_audio)
        self.assertEqual(analyzer.sample_rate, 44100)
        self.assertEqual(analyzer.channels, 2)

    def test_volume_detection(self):
        """测试音量分析逻辑"""
        analyzer = AudioAnalyzer(self.test_audio)
        # 静音文件音量应为 0
        self.assertAlmostEqual(analyzer.get_average_volume(), 0.0, delta=0.01)

    def test_invalid_file(self):
        """测试非法文件处理"""
        with self.assertRaises(ValueError):
            AudioAnalyzer("nonexistent.wav")


if __name__ == "__main__":
    unittest.main()