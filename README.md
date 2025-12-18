<h1>Project Description</h1>

This project is an Auto-Domain Adaptive AI Assistant built using Gemini 3 on Vertex AI and Streamlit.

The system automatically understands the domain, tone, and communication style of a business from uploaded data such as PDFs, CSV/Excel files, images, and website URLs, and then configures itself as a domain-specific AI assistant.

Unlike traditional chatbots or RAG-based systems, the assistant does not retrieve information from documents during every query. Instead, the uploaded data is used only once to configure the assistant’s behavior and persona.

Key Features

Multi-source input support
Accepts multiple PDFs, CSV/Excel files, images, and URLs together.

Automatic domain detection
The assistant identifies the business domain without manual selection.

Dynamic persona and tone adaptation
Adjusts its response style based on the inferred domain
(e.g., friendly for cafés, calm and empathetic for mental wellness).

One-time configuration model
Documents are used during initialisation only, not for per-question retrieval.

Multimodal reasoning with Gemini 3
Text, images, tables, and web content are understood in a single reasoning context.

No RAG or vector database
No embeddings, no chunking, and no document search during chat.

How It Works

The user uploads business-related data (PDFs, tables, images, or URLs).

Gemini 3 analyses all inputs together to infer:

domain

tone

communication boundaries

A domain-specific assistant persona is generated.

All user interactions are answered through this dynamically created persona.

Why This Is Different

This project focuses on behaviour alignment, not document retrieval.
It simplifies AI adoption by removing the need for prompt engineering and heavy retrieval infrastructure, while still producing domain-aware and contextually appropriate responses.
