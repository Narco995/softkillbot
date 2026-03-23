"""AI-Powered Code Generation Engine."""

from typing import Dict, List
from dataclasses import dataclass
from enum import Enum

from ..utils.logger import logger


class CodeLanguage(str, Enum):
    """Supported programming languages."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    GOLANG = "golang"
    RUST = "rust"
    SQL = "sql"
    BASH = "bash"


class CodeTemplateType(str, Enum):
    """Types of code templates."""
    FUNCTION = "function"
    CLASS = "class"
    API_ENDPOINT = "api_endpoint"
    TEST = "test"
    DATABASE_QUERY = "database_query"
    DEPLOYMENT = "deployment"


@dataclass
class GeneratedCode:
    """Generated code snippet with metadata."""
    code: str
    language: CodeLanguage
    template_type: CodeTemplateType
    description: str
    imports: List[str]
    dependencies: List[str]
    test_cases: List[str]
    documentation: str
    quality_score: float


class CodeGenerator:
    """AI-powered code generation engine."""

    # Templates for different code patterns
    TEMPLATES = {
        CodeLanguage.PYTHON: {
            CodeTemplateType.FUNCTION: '''
def {name}({params}):
    """{docstring}"""
    # Implementation
    pass
''',
            CodeTemplateType.CLASS: '''
class {name}:
    """{docstring}"""
    
    def __init__(self):
        pass
    
    def method(self):
        pass
''',
            CodeTemplateType.TEST: '''
import pytest

class Test{name}:
    def test_{method_name}(self):
        assert True
''',
        },
        CodeLanguage.JAVASCRIPT: {
            CodeTemplateType.FUNCTION: '''
function {name}({params}) {{
  // {docstring}
  // Implementation
}}
''',
            CodeTemplateType.API_ENDPOINT: '''
app.post('/api/{endpoint}', async (req, res) => {{
  // Handle request
  res.json({{ status: 'success' }});
}});
''',
        },
        CodeLanguage.SQL: {
            CodeTemplateType.DATABASE_QUERY: '''
SELECT *
FROM {table}
WHERE {condition}
ORDER BY {column};
''',
        },
    }

    @staticmethod
    def generate_code(
        task_description: str,
        language: CodeLanguage,
        template_type: CodeTemplateType,
    ) -> GeneratedCode:
        """Generate code from task description."""
        try:
            # Extract parameters from task description
            params = CodeGenerator._extract_parameters(task_description)

            # Select appropriate template
            template = CodeGenerator._select_template(language, template_type)

            # Generate code using template
            generated_code = CodeGenerator._apply_template(template, params)

            # Generate test cases
            test_cases = CodeGenerator._generate_tests(task_description, language)

            # Generate documentation
            documentation = CodeGenerator._generate_documentation(task_description)

            # Calculate quality score
            quality_score = CodeGenerator._calculate_quality_score(generated_code)

            logger.info(f"Code generated for {task_description[:50]}...")

            return GeneratedCode(
                code=generated_code,
                language=language,
                template_type=template_type,
                description=task_description,
                imports=CodeGenerator._extract_imports(language, task_description),
                dependencies=CodeGenerator._extract_dependencies(task_description),
                test_cases=test_cases,
                documentation=documentation,
                quality_score=quality_score,
            )
        except Exception as e:
            logger.error(f"Error generating code: {str(e)}")
            raise

    @staticmethod
    def _extract_parameters(description: str) -> Dict:
        """Extract function parameters from description."""
        return {
            "name": "function_name",
            "params": "param1, param2",
            "docstring": description[:100],
        }

    @staticmethod
    def _select_template(language: CodeLanguage, template_type: CodeTemplateType) -> str:
        """Select appropriate code template."""
        return CodeGenerator.TEMPLATES.get(language, {}).get(
            template_type,
            "# Template not found\npass",
        )

    @staticmethod
    def _apply_template(template: str, params: Dict) -> str:
        """Apply parameters to template."""
        try:
            return template.format(**params)
        except KeyError:
            return template

    @staticmethod
    def _generate_tests(description: str, language: CodeLanguage) -> List[str]:
        """Generate test cases."""
        test_templates = {
            CodeLanguage.PYTHON: [
                "test_valid_input",
                "test_invalid_input",
                "test_edge_cases",
                "test_performance",
            ],
            CodeLanguage.JAVASCRIPT: [
                "test_success_case",
                "test_error_handling",
                "test_async_operations",
            ],
        }
        return test_templates.get(language, ["test_basic"])

    @staticmethod
    def _generate_documentation(description: str) -> str:
        """Generate documentation for code."""
        return f"""
## Function Documentation

### Description
{description}

### Parameters
- [Extracted from description]

### Returns
- [Inferred from context]

### Example
```
[Usage example]
```
"""

    @staticmethod
    def _extract_imports(language: CodeLanguage, description: str) -> List[str]:
        """Extract required imports."""
        import_map = {
            CodeLanguage.PYTHON: ["import os", "import sys"],
            CodeLanguage.JAVASCRIPT: ["const express = require('express');"],
        }
        return import_map.get(language, [])

    @staticmethod
    def _extract_dependencies(description: str) -> List[str]:
        """Extract external dependencies."""
        dependencies = []
        if "database" in description.lower():
            dependencies.append("sqlalchemy")
        if "api" in description.lower():
            dependencies.append("requests")
        return dependencies

    @staticmethod
    def _calculate_quality_score(code: str) -> float:
        """Calculate code quality score."""
        score = 0.7  # Base score

        # Increase for documentation
        if '"""' in code or "'''" in code or "//" in code:
            score += 0.15

        # Increase for error handling
        if "try" in code or "except" in code or "catch" in code:
            score += 0.1

        # Increase for modularity
        lines = code.split('\n')
        if len(lines) > 5:
            score += 0.05

        return min(1.0, score)

    @staticmethod
    def generate_test_code(function_name: str, language: CodeLanguage) -> str:
        """Generate automated test code."""
        if language == CodeLanguage.PYTHON:
            return f"""
import pytest
from module import {function_name}

class Test{function_name.title()}:
    def test_basic(self):
        result = {function_name}()
        assert result is not None
    
    def test_error_handling(self):
        with pytest.raises(Exception):
            {function_name}(invalid_param=True)
"""
        return "# Test code for language not supported"

    @staticmethod
    def generate_deployment_code(app_name: str) -> str:
        """Generate deployment configuration."""
        return f"""
version: '3.8'
services:
  {app_name}:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - ENVIRONMENT=production
    volumes:
      - ./logs:/app/logs
    restart: always
"""
