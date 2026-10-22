# 📚 Smart Digital Library & Book Recommendation System

A modular desktop-based **Smart Digital Library System** engineered in Python utilizing a strict **Model-View-Controller (MVC)** architecture and **Tkinter GUI**. The platform offers role-based administrative catalog management, transaction safeguards, and an adaptive user recommendation engine powered by frequency analysis and fallback heuristics.

---

## 🌟 Key Features

### 👑 Admin Module
* **Dynamic Catalog Management**: Create new collection items with automatic ID generation (, , etc.) via the Factory Pattern.
* **Smart Data Mutation & State Hygiene**: Modify existing book details with automated edit-form state clearing to prevent unintentional data overwrite.
* **Transactional Deletion Safeguard**: Rejects deletion of catalog items currently registered in active user borrowing lists ().
* **Active Loan Monitor**: Live tracking of current book loans mapped to active user accounts.

### 👤 Reader/User Module
* **Role-Based Authentication**: Isolated user dashboards with tailored views and privileges.
* **Catalog Exploration & Live Search**: Non-case-sensitive search across Book ID, Title, and Author fields.
* **Loan Transactions**: Single-click book borrowing and returning logic with active inventory adjustments ( / ).
* **Personalized Recommendations**: Machine-calculated reading suggestions based on user transaction histories.

---

## 🏗️ Software Architecture & Design Patterns

The project follows high-grade software engineering standards to deliver maintainability, fault tolerance, and testability.



### 1. Directed Acyclic Graph (DAG) & Anti-Circular Import Design
The codebase is decoupled into 4 modular files forming a 1-way acyclic dependency hierarchy. The  module contains zero imports of  or . Instead, interactions are bridged through **Runtime Dependency Injection**.

### 2. Model-View-Controller (MVC) Separation
* **Model ()**: Pure Python business logic and in-memory persistence layer. Completely isolated from Tkinter dependencies.
* **View ()**: Presentation layer built strictly using Tkinter  to eliminate layout freezing and thread competition.
* **Controller ()**: Central orchestrator connecting user interface events to model queries.

### 3. Object-Oriented Design Patterns
* **Singleton Pattern**: The  class overrides  to guarantee a single globally shared data repository instance in memory.
* **Factory Pattern**: The  class uses a  () to dynamically instantiate concrete  or  objects based on catalog category.
* **Pure Dynamic Polymorphism**: The abstract concept class  is extended by  and . Methods  and  are overridden across child classes, enabling the View layer to render item-specific fields dynamically without  branching or  type checking (**Open/Closed Principle**).

---

## 🧮 Book Recommendation Algorithm

The recommendation module implements a dual-mode strategy depending on the user's transaction profile:



1. **Active/Returning User Mode (Frequency Mode Calculation)**
   * Reads the user's persistent transaction log ().
   * Extracts category tags and identifies the most frequent reading genre using .
   * Filters the collection for unread books matching this dominant genre.

2. **New User Mode (Adaptive Fallback Slicing)**
   * When no borrowing history exists, the engine gracefully transitions to a fallback heuristic.
   * Leverages Python list slicing  to deliver the 3 newest catalog entries.

---

## 📂 Project Structure



---

## 🚀 Getting Started

### Prerequisites
* Python 3.10 or higher
* Standard Python libraries (Tkinter and  come pre-installed with standard Python distributions).

### Installation & Execution
1. **Clone the repository:**
   

2. **Run the application:**
   

3. **Default Login Credentials:**
   * **Admin Access**: Username  | Password 
   * **User Access**: Username  | Password 
   * **User Access (New User)**: Username  | Password 

---

## 👥 Team & Contributions

This project was developed for the **Object-Oriented Programming Practicum (PBO)** course at **Universitas Gadjah Mada (UGM)**.

* **Muhammad Daffa Izdihar** — Lead Software Engineer
  * Designed the core MVC architecture, modular multi-file refactoring (DAG pattern), design pattern implementations (Singleton, Factory, Polymorphism), and recommendation algorithms.
* **Salma Nur Rodiah** — System Analyst & Documentation
  * System flowchart design, feature requirement mapping, and project report compilation.
* **Nathania Shira Indah Rosalind** — UI/UX & Quality Assurance
  * Flowchart modeling, presentation slide creation, and application testing/verification.

**Academic Information:**
* **Program**: Applied Bachelor in Internet Engineering Technology (*Sarjana Terapan Teknologi Rekayasa Internet*)
* **Department**: Department of Electrical Engineering and Informatics (DTEDI), Vocational College
* **University**: Universitas Gadjah Mada (UGM), Yogyakarta, Indonesia
* **Course Supervisor**: Dr. Sahirul Alam, S.T., M.Eng.
