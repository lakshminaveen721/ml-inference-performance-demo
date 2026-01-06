# 🚀 Production-Style ML Inference Performance & MLOps System

## 📌 Overview

This project implements a **production-style machine learning inference system** with a strong focus on **performance engineering, observability, and MLOps best practices**.

Instead of optimizing model accuracy, the system is designed to **measure, optimize, and enforce inference performance guarantees** such as **latency, throughput, and regression prevention** — challenges that dominate real-world ML systems in **2026**.

---

## 🎯 Key Problems Addressed

- High **tail latency** (p95 / p99) under load  
- **GPU underutilization** in inference workloads  
- Lack of **observability** in ML services  
- **Silent performance regressions** after code changes  

---

## 🏗️ System Architecture

Client / Load Generator
|
v
FastAPI Inference Service
|
v
Dynamic Batching Queue
|
v
PyTorch Model (CPU / GPU, FP32 / FP16)

Observability:
Inference → Prometheus Metrics

Reliability:
CI Performance Regression Gates (GitHub Actions)


---

## ⚙️ Core Features

### 🔹 Real-Time Inference Service
- FastAPI-based inference API  
- CPU and GPU compatible  
- Single-worker design to expose real bottlenecks  

---

### 🔹 Performance Observability
- Latency histograms (p50 / p95 / p99)  
- Request and error counters  
- `/metrics` endpoint for Prometheus scraping  

---

### 🔹 Dynamic Request Batching
- Micro-batching with configurable:
  - batch size
  - batching window  
- Amortizes framework and kernel launch overhead  
- Achieved **3×+ throughput improvement** under load  

---

### 🔹 Precision-Aware Execution
- Runtime precision switching:
  - **FP32** — safe / debug mode  
  - **FP16** — high-performance mode  
- Controlled via environment variables  

---

### 🔹 CI-Based Performance Regression Gates
- GitHub Actions pipeline runs on every PR  
- Automatically:
  - starts the inference service  
  - waits for service readiness  
  - executes a performance benchmark  
- Fails the build if **latency budgets** are exceeded  
- Prevents silent performance degradation  

---

## 📊 Representative Performance Results

| Metric | Before Batching | After Batching |
|------|-----------------|----------------|
| Avg latency | ~100 ms | ~25 ms |
| p99 latency | ~464 ms | Significantly reduced |
| Throughput | Baseline | **3×+ increase** |
| GPU utilization | Low | Substantially higher |

---

## 🧪 Performance Enforcement in CI

Performance is treated as a **first-class contract**, not a best-effort metric.

Example enforced budgets:
- Average latency ≤ **250 ms**
- p95 latency ≤ **500 ms**

Builds fail automatically if these budgets are violated.

---

## 🛠️ Tech Stack

- **Python**, **FastAPI**
- **PyTorch**, **TorchVision**
- **Prometheus** (metrics & observability)
- **GitHub Actions** (CI/CD)
- **Custom dynamic batching implementation**

---

## 🧠 Why This Project Matters

This project mirrors how **real ML platform and AI infrastructure teams** operate:

- Models are treated as black boxes  
- Performance is measured, not assumed  
- Optimizations are data-driven  
- Regressions are caught automatically  

---

## 🚦 Future Extensions (Optional)

- Plug in external NLP / vision models  
- Multi-model routing and benchmarking  
- Cost-aware autoscaling  
- LLM inference optimization  

---

## 📜 License

MIT
