# Project: "Barry Sharp's Pro Mover" - AI Dev Team Build Plan

**Version:** 1.0
**Date:** May 26, 2025
**Goal:** To construct a hybrid team of AI Agents within LangFlow, leveraging local models (respecting hardware constraints) and Google Gemini models (via Google AI Studio API), emulating a game development studio structure to assist in building "Barry Sharp's Pro Mover."
**Philosophy:** We will build iteratively, starting with core infrastructure and a single workflow slice, then expanding capabilities and adding departments. We will prioritize a robust orchestration layer (our "MCP" or Project Manager) and a solid knowledge base (RAG). Human-in-the-loop is central to every phase.
**Hardware Constraints:** MacBook M2, 16GB RAM, macOS Sequoia. This means we *must* be judicious with local models. We will rely heavily on **Ollama** for managing local models and aim to run only *one* (or at most two very small) local models *simultaneously*. We will select smaller, quantized models (e.g., 4-bit quantized 7B or 3B models).

---

## Phase 0: Setup & Foundation

**Goal:** Prepare the local environment, install necessary tools, and gather credentials.

**Steps:**

1.  **Install Homebrew (if not present):**
    * Open Terminal.
    * Run: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
    * Follow instructions.
2.  **Install Python (if needed):**
    * Ensure you have Python 3.9+ (LangFlow often works best with slightly older, stable versions).
    * Run: `brew install python`
    * Consider setting up a virtual environment: `python3 -m venv langflow_env` and `source langflow_env/bin/activate`.
3.  **Install LangFlow:**
    * Run: `pip install langflow`
4.  **Install Ollama:**
    * Visit `ollama.com` and download the macOS application.
    * Install and run it. You should see the Ollama icon in your menu bar.
5.  **Pull Initial Local Models (Start Small!):**
    * Open Terminal.
    * Run: `ollama pull mistral:7b-instruct-q4_K_M` (Good all-rounder, 4-bit quantized medium size - should fit 16GB RAM).
    * Run: `ollama pull phi3:mini-instruct` (Very small, good for simple tasks/QA ideas).
    * Run: `ollama pull nomic-embed-text` (Needed for local RAG embedding).
6.  **Get Google AI Studio API Key:**
    * Visit `aistudio.google.com`.
    * Log in with your Google account.
    * Click "Get API Key" -> "Create API key in new project."
    * Copy the key and store it securely (e.g., in a password manager or environment variable, *not* in your code directly).
7.  **Create Project Directory Structure:**
    * Create a main folder (e.g., `BarrySharpProMover`).
    * Inside, create folders: `docs`, `langflow_projects`, `assets`, `scripts`, `vectorstore`.
8.  **Prepare Initial Documents:**
    * Place your Game Design Document (GDD) and any "Development Rules" or "Design Standards" into the `docs` folder.

**Validation 0:**

* Run `langflow run` in Terminal. Ensure you can access the LangFlow UI in your browser (usually `http://127.0.0.1:7860`).
* Run `ollama run mistral` in Terminal. Ensure you can chat with the local Mistral model.
* Check that your Google AI Studio API key is saved.

---

## Phase 1: Knowledge Base (RAG) Setup

**Goal:** Create a vector store from your GDD and rules so agents can access project-specific information.

**Steps:**

1.  **Launch LangFlow.**
2.  **Create a New Project: `RAG_Builder`**.
3.  **Add Components:**
    * `DirectoryLoader`: Point it to your `docs` folder. Set `glob` to `**/*.md` or `**/*.txt` depending on your doc format.
    * `RecursiveCharacterTextSplitter`: Connect `DirectoryLoader` to it. Configure chunk size (e.g., 1000) and overlap (e.g., 200).
    * `OllamaEmbeddings`: Add this component. Set `Model` to `nomic-embed-text`.
    * `FAISS`: Connect `RecursiveCharacterTextSplitter` (Documents) and `OllamaEmbeddings` (Embeddings) to it. Set `Folder path` to your `vectorstore` directory and `Index name` to `barrysharp_kb`.
4.  **Run the Flow:** Click the "play" or "run" button. This will process your documents and create the FAISS index files in your `vectorstore` folder.
5.  **Create a New Project: `RAG_Tester`**.
6.  **Add Components:**
    * `TextInput`: For asking questions.
    * `OllamaEmbeddings`: Set `Model` to `nomic-embed-text`.
    * `FAISS`: Set `Folder path` and `Index name` as before. Set `Input Type` to `Retriever`. Connect `OllamaEmbeddings`.
    * `PromptTemplate`: Create a template like: "Based on this context:\n{context}\n\nAnswer this question: {question}".
    * `ChatOllama`: Connect `PromptTemplate`. Set `Model` to `mistral:7b-instruct-q4_K_M`. Set `Temperature` to 0.2 (for factual answers).
    * `VectorStoreInfo`: Connect `FAISS` (Retriever) to `VectorStoreInfo`.
    * `VectorStoreAgent`: Connect `ChatOllama` (LLM) and `VectorStoreInfo` (VectorStoreInfo). Connect `TextInput` (Input) to it.
    * `TextOutput`: Connect `VectorStoreAgent` to it.
7.  **Test RAG:** Use the `TextInput` to ask questions about your GDD (e.g., "What is the core mechanic?").

**Validation 1:**

* Check that index files (`.faiss`, `.pkl`) are created in your `vectorstore` directory.
* Confirm that the `RAG_Tester` flow provides answers based *specifically* on your documents, not just general knowledge.

---

## Phase 2: Core Agent Components Test

**Goal:** Ensure LangFlow can reliably communicate with both Gemini and a local Ollama model.

**Steps:**

1.  **Create a New Project: `API_Test`**.
2.  **Add Components:**
    * `TextInput`.
    * `GoogleGenerativeAI`: Enter your Google AI Studio API Key. Select a model like `gemini-1.5-flash-latest` (fast, cost-effective). Connect `TextInput`.
    * `TextOutput`: Connect `GoogleGenerativeAI`.
3.  **Test Gemini:** Enter a prompt and verify you get a response.
4.  **Create a New Project: `Local_Test`**.
5.  **Add Components:**
    * `TextInput`.
    * `ChatOllama`: Set `Model` to `mistral:7b-instruct-q4_K_M`. Connect `TextInput`.
    * `TextOutput`: Connect `ChatOllama`.
6.  **Test Ollama:** Enter a prompt and verify you get a response. Ensure Ollama is running in the background.

**Validation 2:**

* Both test flows successfully generate responses from their respective models.

---

## Phase 3: The Orchestrator (MCP / PM Agent - V1)

**Goal:** Build a *basic* central agent in LangFlow that can take input and call *one* other (dummy) flow, managing minimal state. This will be Python-heavy.

**Steps:**

1.  **Create a Dummy Department Flow (e.g., `Design_Dummy`):**
    * `TextInput`.
    * `ChatOllama` (Mistral). Add a simple prompt like "You are a game designer. Acknowledge this task: {input_text}".
    * `TextOutput`.
    * Export this flow (`Export` button) and save it as `design_dummy.json` in `langflow_projects`.
2.  **Create a New Project: `MCP_V1`**.
3.  **Add `TextInput`:** This will be your input to the PM.
4.  **Add `CustomComponent` (Python):** This is our PM/MCP core.
    * **Code:**
        ```python
        from langflow.base.flow_processing.utils import process_data_from_flow
        from langflow.load import run_flow_from_json
        import json
        import os

        # Define project base path (adjust if needed)
        PROJECT_BASE = './'
        STATE_FILE = os.path.join(PROJECT_BASE, 'project_state.json')

        def load_state():
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, 'r') as f:
                    return json.load(f)
            return {"phase": "start", "task": None, "results": {}}

        def save_state(state):
            with open(STATE_FILE, 'w') as f:
                json.dump(state, f, indent=2)

        def build_flow(input_text: str) -> str:
            state = load_state()

            # Simple logic: If start, set task and call Design
            if state["phase"] == "start":
                state["task"] = input_text
                state["phase"] = "design_pending"
                save_state(state)

                # --- Call the dummy flow ---
                # NOTE: This requires Langflow to support calling sub-flows.
                # If direct calls aren't stable, this might need an API call
                # back to Langflow or external Python scripting.
                # For now, we simulate the call & return a message.
                # In a real version, we'd use run_flow_from_json or similar
                # and capture its output.
                try:
                    # Placeholder - Real implementation needs flow running
                    # design_flow_path = os.path.join(PROJECT_BASE, 'langflow_projects', 'design_dummy.json')
                    # result = run_flow_from_json(flow=design_flow_path, input_value=input_text, tweaks=None)
                    # design_output = result[0].outputs[0].text # Example path
                    design_output = f"Design team acknowledged: {input_text}"
                    state["results"]["design"] = design_output
                    state["phase"] = "design_complete"
                    save_state(state)
                    return f"PM: Sent task to Design. They said: '{design_output}'"

                except Exception as e:
                    return f"PM: Error calling Design flow: {e}"

            elif state["phase"] == "design_complete":
                 return f"PM: Design is complete. Task was: {state['task']}. Result: {state['results']['design']}. Ready for next step (not implemented)."

            else:
                return f"PM: Current state: {state['phase']}. No action defined."

        ```
    * Connect `TextInput` to `build_flow`'s `input_text`.
5.  **Add `TextOutput`:** Connect the `CustomComponent` output to it.

**Validation 3:**

* Run `MCP_V1`. Provide an initial task.
* Check that `project_state.json` is created/updated.
* Verify the output indicates the (simulated) call to the design flow.
* Run it again. Verify it acknowledges the "design_complete" state.
* *Self-Correction:* Realizing `run_flow_from_json` might be tricky *inside* LangFlow, we acknowledge the V1 uses a simulation. V2 will need a robust way to call sub-flows (maybe via LangFlow's API or a LangChain/LiteLLM layer).

---

## Phase 4: Department 1 (Design - V1)

**Goal:** Build a real, hybrid Design department flow and integrate it with the PM.

**Steps:**

1.  **Create `Design_V1` Flow:**
    * `TextInput` (Task from PM).
    * `PromptTemplate` (Gemini Ideation): "You are Gemini 1.5 Pro, a brilliant game designer. Based on our GDD (context_placeholder) and this task: '{input_text}', generate 5 creative mechanic variations."
    * `GoogleGenerativeAI`: Connect `PromptTemplate`.
    * `PromptTemplate` (Local Filtering): "You are Mistral-7B, a pragmatic designer focused on GB Studio limits (4-buttons, simple physics, NES-style). Review these 5 ideas: '{gemini_output}'. Also consider our rules (context_placeholder). Select the top 2 ideas that fit these constraints and explain why."
    * `ChatOllama` (Mistral): Connect `PromptTemplate`.
    * `TextOutput` (Filtered ideas to PM).
    * **RAG Integration:** Add `FAISS` (Retriever) and connect it to *both* `PromptTemplate` components to provide the `context_placeholder`. You'll need to structure the input to these prompts to include the RAG context.
2.  **Modify `MCP_V1` (Now `MCP_V2`):**
    * Update the Python code in the `CustomComponent` to *actually* call `Design_V1` (using LangFlow's API if necessary, or a Python function that builds and runs the chain if `run_flow_from_json` isn't feasible internally).
    * Implement logic to present the `Design_V1` output to the user (via the `TextOutput`) and wait for an "Approve" or "Revise" input. This requires a more complex state machine and potentially a chat-like interface or multiple input points.

**Validation 4:**

* Give the PM a design task (e.g., "Design 5 grappling hook variants").
* Verify the PM calls `Design_V1`.
* Check that `Design_V1` uses both Gemini and Mistral.
* Confirm the PM presents the filtered results to you.
* Ensure the RAG context is being pulled in.
* *Crucially:* Monitor your Mac's Activity Monitor. Ensure RAM usage stays manageable. If Mistral 7B is too large, consider `phi3:mini` or smaller quantized models. **Only run *one* local model at a time if necessary.**

---

## Phase 5: Memory Layer (V1)

**Goal:** Add persistent memory and conversation history.

**Steps:**

1.  **Enhance `MCP_V2` (`MCP_V3`):**
    * Modify the PM's Python code:
        * Save *more* detailed state to `project_state.json` (current task, history of actions, outputs from each dept).
        * Implement a simple chat history mechanism. When calling an agent, provide the last few turns of relevant conversation or the approved outputs from the previous phase.
2.  **Add LangFlow Memory Components:**
    * Explore using `ConversationBufferMemory` or `FileChatMessageHistory` within specific department flows *if* they need conversational context for *their specific sub-task*. However, the *primary, long-term* memory should reside with the PM.

**Validation 5:**

* Run a multi-step task (e.g., Design -> Approve).
* Restart LangFlow or the flow.
* Check if the PM remembers the current state from `project_state.json`.
* Verify that if you ask an agent a follow-up, it has some context from the previous step.

---

## Phase 6-10: Building Other Departments & Enhancing

**Goal:** Iteratively build the Art, Code, QA, and Asset Manager departments, and implement the "2-agent collaboration" and PM enhancements.

**General Steps for Each Department (V1):**

1.  **Select Models:** Choose one API (Gemini) and one *small* local model (Phi-3 or similar, *or* reuse Mistral if possible, *or* use another Gemini prompt for critique if local resources are tight). For Art, consider Gemini Vision for critique and maybe an API like Stability AI or manual creation initially, as local SDXL is likely too heavy for 16GB RAM alongside LLMs.
2.  **Build Flow:** Create the LangFlow graph, incorporating RAG and prompts for generation/critique.
3.  **Integrate with PM:** Update the PM's Python code to call the new department flow in the correct sequence and handle its output/approval.
4.  **Test & Validate:** Run the workflow, monitor resources.

**Specific Enhancements (V2):**

1.  **2-Agent Collaboration:** Within each department flow, explicitly chain the "Generator" agent's output into the "Critic" agent's input with a specific critique/refinement prompt.
2.  **PM Routing:** Make the PM's logic smarter, perhaps using an LLM call itself to decide the next step based on the current state and user feedback.
3.  **Error Handling & Fallbacks:** Add `try...except` blocks in the PM to handle API errors or flow failures. Implement a *simple* fallback (e.g., if Gemini fails, try Mistral with a modified prompt).

**Validation 6-10:**

* Each department successfully performs its core task within the workflow.
* The PM correctly routes tasks and results.
* The "2-agent" chains produce (hopefully) better results than a single agent.
* RAM usage remains under control. You might need to implement logic in your PM Python code to *explicitly tell Ollama (via its API) to load/unload models* if necessary, though this adds significant complexity. A simpler approach is to *design* your flows so only one local model is needed per step.

---

## Phase 11: Full Testing & Refinement

**Goal:** Test the entire system end-to-end and optimize.

**Steps:**

1.  **Run a Full Scenario:** Take a small feature (e.g., adding a 'jump' mechanic) through the *entire* workflow from Design to QA.
2.  **Identify Bottlenecks:** Where does it get stuck? Which agents underperform? Is the PM logic flawed?
3.  **Optimize Prompts:** This is *key*. Refine the prompts for each agent based on its performance. Add examples, improve context, clarify instructions.
4.  **Tune Flows:** Adjust LangFlow configurations. Maybe one agent needs a higher temperature, another needs a stricter prompt.
5.  **Resource Check:** Perform a final check on resource usage. Can you run the most common workflows without a crash?

**Validation 11:**

* The system can successfully process at least one simple feature from start to finish with your intervention.
* You have a clear understanding of its strengths and weaknesses.
* It demonstrably assists in your development process.

---

**This is an ambitious plan, but by building it piece by piece and validating each step, it's achievable.** The biggest challenges will be the PM/Orchestration logic and managing local model resources. Be prepared to adapt, simplify, and iterate! This is going to be an exciting journey into building your AI-powered development team! Let's fire up LangFlow and start with Phase 0/1!
