"""
PROC LANGUAGE Implementation for Open-SAS

This module implements SAS PROC LANGUAGE functionality for LLM integration
using Ollama for open-source language model access.
"""

import pandas as pd
import numpy as np
import requests
import json
from typing import Dict, List, Any, Optional
from ..parser.proc_parser import ProcStatement


class ProcLanguage:
    """Implementation of SAS PROC LANGUAGE procedure."""
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
        self.default_model = "llama2"  # Default Ollama model
    
    def execute(self, data: pd.DataFrame, proc_info: ProcStatement) -> Dict[str, Any]:
        """
        Execute PROC LANGUAGE on the given data.
        
        Args:
            data: Input DataFrame
            proc_info: Parsed PROC statement information
            
        Returns:
            Dictionary containing results and output data
        """
        results = {
            'output_text': [],
            'output_data': None
        }
        
        # Get PROMPT specification
        prompt = proc_info.options.get('prompt', '')
        if not prompt:
            results['output_text'].append("ERROR: PROMPT specification required for PROC LANGUAGE.")
            return results
        
        # Get model specification
        model = proc_info.options.get('model', self.default_model)
        
        # Get mode specification
        mode = proc_info.options.get('mode', 'generate').lower()
        if mode not in ['generate', 'qna', 'summarize', 'analyze']:
            mode = 'generate'
        
        # Get VAR specification for data analysis
        var_vars = proc_info.options.get('var', [])
        
        results['output_text'].append("PROC LANGUAGE - LLM Analysis")
        results['output_text'].append("=" * 50)
        results['output_text'].append(f"Model: {model}")
        results['output_text'].append(f"Mode: {mode.upper()}")
        results['output_text'].append("")
        
        # Check Ollama availability
        if not self._check_ollama_availability():
            results['output_text'].append("ERROR: Ollama is not running or not accessible.")
            results['output_text'].append("Please ensure Ollama is installed and running on localhost:11434")
            results['output_text'].append("Install from: https://ollama.ai/")
            return results
        
        # Check if model is available
        if not self._check_model_availability(model):
            results['output_text'].append(f"ERROR: Model '{model}' is not available in Ollama.")
            results['output_text'].append(f"Available models: {', '.join(self._get_available_models())}")
            results['output_text'].append(f"To install: ollama pull {model}")
            return results
        
        # Execute based on mode
        if mode == 'generate':
            llm_results = self._generate_text(prompt, model)
        elif mode == 'qna':
            context = proc_info.options.get('context', '')
            llm_results = self._question_answer(prompt, context, model)
        elif mode == 'summarize':
            if var_vars:
                llm_results = self._summarize_data(data, var_vars, prompt, model)
            else:
                llm_results = self._summarize_text(prompt, model)
        else:  # analyze
            if var_vars:
                llm_results = self._analyze_data(data, var_vars, prompt, model)
            else:
                llm_results = self._analyze_text(prompt, model)
        
        # Format output
        results['output_text'].extend(llm_results['output'])
        results['output_data'] = llm_results.get('data', None)
        
        return results
    
    def _check_ollama_availability(self) -> bool:
        """Check if Ollama is running and accessible."""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _check_model_availability(self, model: str) -> bool:
        """Check if a specific model is available in Ollama."""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                return any(m['name'].startswith(model) for m in models)
            return False
        except:
            return False
    
    def _get_available_models(self) -> List[str]:
        """Get list of available models in Ollama."""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                return [m['name'] for m in models]
            return []
        except:
            return []
    
    def _generate_text(self, prompt: str, model: str) -> Dict[str, Any]:
        """Generate text using the LLM."""
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get('response', '')
                
                output = []
                output.append("Text Generation")
                output.append("-" * 20)
                output.append(f"Prompt: {prompt}")
                output.append("")
                output.append("Generated Response:")
                output.append("-" * 20)
                output.append(generated_text)
                output.append("")
                
                return {
                    'output': output,
                    'data': {'generated_text': generated_text}
                }
            else:
                return {
                    'output': [f"ERROR: Ollama API returned status {response.status_code}"],
                    'data': None
                }
                
        except Exception as e:
            return {
                'output': [f"ERROR: Failed to generate text - {str(e)}"],
                'data': None
            }
    
    def _question_answer(self, question: str, context: str, model: str) -> Dict[str, Any]:
        """Perform question-answering using the LLM."""
        if not context:
            return {
                'output': ["ERROR: CONTEXT is required for question-answering mode"],
                'data': None
            }
        
        # Combine context and question
        full_prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
        
        return self._generate_text(full_prompt, model)
    
    def _summarize_text(self, text: str, model: str) -> Dict[str, Any]:
        """Summarize text using the LLM."""
        prompt = f"Please provide a concise summary of the following text:\n\n{text}"
        return self._generate_text(prompt, model)
    
    def _summarize_data(self, data: pd.DataFrame, var_vars: List[str], prompt: str, model: str) -> Dict[str, Any]:
        """Summarize data using the LLM."""
        # Prepare data summary
        if not var_vars:
            var_vars = data.select_dtypes(include=[np.number]).columns.tolist()
        
        data_summary = data[var_vars].describe()
        
        # Create text summary
        summary_text = f"Data Summary for variables: {', '.join(var_vars)}\n\n"
        summary_text += data_summary.to_string()
        
        # Add prompt context
        full_prompt = f"Data Summary:\n{summary_text}\n\nUser Request: {prompt}\n\nPlease provide insights based on this data:"
        
        return self._generate_text(full_prompt, model)
    
    def _analyze_text(self, text: str, model: str) -> Dict[str, Any]:
        """Analyze text using the LLM."""
        prompt = f"Please analyze the following text and provide insights:\n\n{text}"
        return self._generate_text(prompt, model)
    
    def _analyze_data(self, data: pd.DataFrame, var_vars: List[str], prompt: str, model: str) -> Dict[str, Any]:
        """Analyze data using the LLM."""
        # Prepare comprehensive data analysis
        if not var_vars:
            var_vars = data.select_dtypes(include=[np.number]).columns.tolist()
        
        analysis_text = f"Data Analysis for variables: {', '.join(var_vars)}\n\n"
        
        # Add descriptive statistics
        analysis_text += "Descriptive Statistics:\n"
        analysis_text += data[var_vars].describe().to_string()
        analysis_text += "\n\n"
        
        # Add correlation matrix if multiple numeric variables
        numeric_vars = data[var_vars].select_dtypes(include=[np.number]).columns
        if len(numeric_vars) > 1:
            analysis_text += "Correlation Matrix:\n"
            analysis_text += data[numeric_vars].corr().to_string()
            analysis_text += "\n\n"
        
        # Add missing data info
        missing_info = data[var_vars].isnull().sum()
        if missing_info.sum() > 0:
            analysis_text += "Missing Data:\n"
            analysis_text += missing_info.to_string()
            analysis_text += "\n\n"
        
        # Add prompt context
        full_prompt = f"Data Analysis:\n{analysis_text}\n\nUser Request: {prompt}\n\nPlease provide statistical insights and recommendations:"
        
        return self._generate_text(full_prompt, model)
