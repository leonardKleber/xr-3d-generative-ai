#
# SPDX-FileCopyrightText: Copyright (c) 1993-2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import logging
from transformers import pipeline
import config

logger = logging.getLogger(__name__)

class GuardrailService:
    """Service for content filtering using NSFW Prompt Detector."""
    
    def __init__(self, model_name="ezb/NSFW-Prompt-Detector"):
        """Initialize the guardrail service with NSFW Prompt Detector."""
        self.model_name = model_name
        self.pipe = None
        self.is_loaded = False
        
    def load_model(self):
        """Load the NSFW Prompt Detector model for content filtering."""
        try:
            if self.is_loaded:
                return True
                
            logger.info(f"Loading NSFW Prompt Detector model: {self.model_name}")
            
            # Load the pipeline
            self.pipe = pipeline("text-classification", model=self.model_name)
            
            self.is_loaded = True
            
            logger.info("✅ NSFW Prompt Detector model loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load NSFW Prompt Detector model: {e}")
            return False
    
    def is_dangerous(self, prompt, threshold):
        """Check if a prompt violates safety policies."""
        try:
            if not self.load_model():
                logger.warning("Guardrail model not loaded, skipping content check")
                return False
            
            # Use the pipeline to classify the prompt
            result = self.pipe(prompt)
            
            # The model returns a score indicating NSFW content
            score = result[0]["score"]
            label = result[0]["label"]
            
            logger.info(f"Content safety score for prompt: {score:.4f} (label: {label})")
            
            return label == "NSFW" and score > threshold
            
        except Exception as e:
            logger.error(f"Error in content safety check: {e}")
            # In case of error, err on the side of caution and flag the content
            return True
    
    def check_prompt_safety(self, prompt, threshold=0.9):
        """Check if a prompt is safe for image generation."""
        try:
            is_violation = self.is_dangerous(prompt, threshold)
            
            if is_violation:
                logger.warning(f"2D prompt flagged as inappropriate: {prompt[:100]}...")
                return False, "PROMPT_CONTENT_FILTERED"
            else:
                logger.info(f"2D prompt passed safety check: {prompt[:100]}...")
                return True, "Content is safe for image generation"
                
        except Exception as e:
            logger.error(f"Error checking prompt safety: {e}")
            # In case of error, err on the side of caution
            return False, "Error in content safety check, please try again" 