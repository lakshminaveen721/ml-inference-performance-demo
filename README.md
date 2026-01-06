Project Title

Production-Style ML Inference Performance & MLOps System


Overview

This project implements a production-style machine learning inference system with a strong focus on performance engineering, observability, and MLOps best practices.

Rather than optimizing model accuracy, the system is designed to measure, optimize, and enforce inference performance guarantees such as latency, throughput, and regression prevention—problems that dominate real-world ML systems in 2026.


Key Problems Addressed

High tail latency (p95 / p99) under load

GPU underutilization in inference workloads

Lack of observability in ML services

Silent performance regressions after code changes

### SYstem Architecture

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


##Core Features
🔹 Real-Time Inference Service

FastAPI-based inference API

CPU and GPU compatible

Single-worker design to expose true bottlenecks

🔹 Performance Observability

Latency histograms (p50 / p95 / p99)

Request and error counters

/metrics endpoint for Prometheus scraping

🔹 Dynamic Request Batching

Micro-batching with configurable:

batch size

batching window

Amortizes framework and kernel launch overhead

3×+ throughput improvement observed under load

🔹 Precision-Aware Execution

Runtime switch between:

FP32 (safe / debug mode)

FP16 (high-performance mode)

Controlled via environment variables

🔹 CI-Based Performance Regression Gates

GitHub Actions pipeline runs on every PR

Automatically:

starts inference service

waits for readiness

executes a benchmark

Fails build if latency budgets are exceeded

Prevents silent performance degradation


##########
Tech Stack

Python, FastAPI

PyTorch, TorchVision

Prometheus metrics

GitHub Actions (CI)

Dynamic batching (custom implementation)
