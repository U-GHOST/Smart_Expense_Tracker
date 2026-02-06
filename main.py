#!/usr/bin/env python3

'''
Smart Expense Tracker 3rd Year Project for AI.
'''

from datetime import datetime

import streamlit as st
import chromadb

from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from pydantic import BaseModel, Field

# Setup a model
class Expense( BaseModel ):
	amount: float
	desc: str
	category: str
	date: str = Field( default_factory = lambda: datetime.now().strftime( "%Y-%m-%d" ) )

# Init ChromaDB
client = chromadb.PersistentClient( path = "./chroma_data" )
# Connect the DB to Ollama
emb_fn = OllamaEmbeddingFunction(
	model_name = "nomic-embed-text:latest",
	url = "http://localhost:11434/api/embeddings"
)
collection = client.get_or_create_collection( name = "expenses", embedding_function = emb_fn )

# Streamlit UI
st.title( "Smart Expense Tracker" )

with st.sidebar:
	st.header( "Add Expense" )

	amount = st.number_input( "Amount", min_value = 0.0, step = 0.01 )
	desc = st.text_input( "Description (e.g. Coffee)" )
	cat = st.selectbox(
		"Category",

		["Food", "Transport", "Bills", "Rent", "Entertainment"]
	)

	if st.button( "Save Expense" ):
		exp = Expense( amount = amount, desc = desc, category = cat )

		collection.add(
			documents = [f"{exp.date}: {exp.desc} ({exp.category}) - {exp.amount}"],
			ids = [f"{datetime.now().timestamp()}"],
			metadatas = [exp.model_dump()]
		)

		st.success( "Expense Saved!" )

# AI Insights
st.header( "Financial Advisor" )
if st.button( "Analyze My Spending" ):
	# Retrieve all expenses from ChromaDB
	results = collection.get()

	if not results["documents"]:
		st.warning( "No data found. Add some expenses first!" )
	else:
		all_data = "\n".join( results["documents"] )

		# Simple prompt for Ollama
		import ollama

		prompt = f"Here are my recent expenses:\n{all_data}\n\nProvide 3 short, educated suggestions to save money."

		with st.spinner( "Thinking..." ):
			response = ollama.generate( model = "smollm2:135m", prompt = prompt )
			st.markdown( f"### Suggestions:\n{response["response"]}" )
		
# Data View
if st.checkbox( "Show Row Data" ):
	st.write( collection.get() )
