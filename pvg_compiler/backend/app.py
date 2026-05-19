
import os
import glob
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from compiler_service import CompilerService

app = FastAPI(
    title="PVG Compiler Studio API",
    description="REST API dla kompilatora Procedural Vector Graphics (PVG) → SVG",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

compiler = CompilerService()

EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), '..', 'examples')

class CompileRequest(BaseModel):
    code: str
    include_ast: bool = False
    include_tokens: bool = False

class CompileResponse(BaseModel):
    success: bool
    svg: Optional[str] = None
    ast: Optional[dict] = None
    tokens: Optional[list] = None
    errors: list = []
    output: str = ""

class TokenizeRequest(BaseModel):
    code: str

class TokenizeResponse(BaseModel):
    success: bool
    tokens: list = []
    errors: list = []

class ParseRequest(BaseModel):
    code: str

class ParseResponse(BaseModel):
    success: bool
    ast: Optional[dict] = None
    errors: list = []

class ExampleItem(BaseModel):
    name: str
    title: str

class ExampleDetail(BaseModel):
    name: str
    title: str
    code: str

@app.get("/api/health")
async def health_check():
    
    return {"status": "ok", "version": "1.0.0", "compiler": "PVG → SVG"}

@app.post("/api/compile", response_model=CompileResponse)
async def compile_code(request: CompileRequest):
    
    result = compiler.compile(
        code=request.code,
        include_ast=request.include_ast,
        include_tokens=request.include_tokens
    )
    return CompileResponse(**result)

@app.post("/api/tokenize", response_model=TokenizeResponse)
async def tokenize_code(request: TokenizeRequest):
    
    result = compiler.tokenize(code=request.code)
    return TokenizeResponse(**result)

@app.post("/api/parse", response_model=ParseResponse)
async def parse_code(request: ParseRequest):
    
    result = compiler.parse(code=request.code)
    return ParseResponse(**result)

@app.get("/api/examples", response_model=list[ExampleItem])
async def list_examples():
    
    examples = []
    pattern = os.path.join(EXAMPLES_DIR, '*.pvg')

    for filepath in sorted(glob.glob(pattern)):
        filename = os.path.basename(filepath)
        name = filename.replace('.pvg', '')

        title = name.split('_', 1)[-1].replace('_', ' ').title() if '_' in name else name.title()
        examples.append(ExampleItem(name=name, title=title))

    return examples

@app.get("/api/examples/{name}", response_model=ExampleDetail)
async def get_example(name: str):
    
    filepath = os.path.join(EXAMPLES_DIR, f"{name}.pvg")

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail=f"Przykład '{name}' nie został znaleziony.")

    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()

    title = name.split('_', 1)[-1].replace('_', ' ').title() if '_' in name else name.title()
    return ExampleDetail(name=name, title=title, code=code)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
