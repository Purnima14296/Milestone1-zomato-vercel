"""
Phase 7 Health API: System health check endpoints.

This module implements health check endpoints for monitoring system status,
component health, and overall system availability.
"""

from __future__ import annotations

import time
import psutil
from datetime import datetime
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, status

from models import (
    HealthResponse, 
    HealthStatus, 
    ComponentHealth,
    ErrorResponse
)


class HealthAPI:
    """Health check API endpoints."""
    
    def __init__(self):
        self.start_time = time.time()
        self.router = APIRouter(prefix="/api/health", tags=["health"])
        self._setup_routes()
    
    def _setup_routes(self) -> None:
        """Setup health check routes."""
        self.router.add_api_route(
            "/", 
            self.health_check, 
            methods=["GET"],
            response_model=HealthResponse,
            summary="System health check",
            description="Check overall system health and component status"
        )
        
        self.router.add_api_route(
            "/components", 
            self.component_health, 
            methods=["GET"],
            response_model=List[ComponentHealth],
            summary="Component health check",
            description="Check health of individual system components"
        )
        
        self.router.add_api_route(
            "/ping", 
            self.ping, 
            methods=["GET"],
            summary="Ping endpoint",
            description="Simple ping endpoint for availability check"
        )
    
    async def health_check(self) -> HealthResponse:
        """
        Perform comprehensive system health check.
        
        Returns:
            HealthResponse with overall system status and component health
        """
        try:
            # Check individual components
            components = await self._check_all_components()
            
            # Determine overall health status
            overall_status = self._determine_overall_health(components)
            
            # Calculate uptime
            uptime = time.time() - self.start_time
            
            return HealthResponse(
                status=overall_status,
                timestamp=datetime.utcnow(),
                version="1.0.0",
                components=components,
                uptime=uptime
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Health check failed: {str(e)}"
            )
    
    async def component_health(self) -> List[ComponentHealth]:
        """
        Check health of individual system components.
        
        Returns:
            List of ComponentHealth objects
        """
        try:
            return await self._check_all_components()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Component health check failed: {str(e)}"
            )
    
    async def ping(self) -> Dict[str, Any]:
        """
        Simple ping endpoint for availability check.
        
        Returns:
            Ping response with timestamp
        """
        return {
            "status": "ok",
            "timestamp": datetime.utcnow().isoformat(),
            "message": "pong"
        }
    
    async def _check_all_components(self) -> List[ComponentHealth]:
        """Check health of all system components."""
        components = []
        
        # Check database
        components.append(await self._check_database_health())
        
        # Check LLM service
        components.append(await self._check_llm_health())
        
        # Check cache
        components.append(await self._check_cache_health())
        
        # Check file system
        components.append(await self._check_filesystem_health())
        
        # Check system resources
        components.append(await self._check_system_resources_health())
        
        return components
    
    async def _check_database_health(self) -> ComponentHealth:
        """Check database component health."""
        start_time = time.time()
        
        try:
            # Simulate database health check
            # In real implementation, this would check actual database connection
            await self._simulate_database_query()
            
            response_time = time.time() - start_time
            
            return ComponentHealth(
                name="database",
                status=HealthStatus.HEALTHY,
                response_time=response_time,
                message="Database connection successful",
                details={"connection_pool": "active", "query_time": response_time}
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            
            return ComponentHealth(
                name="database",
                status=HealthStatus.UNHEALTHY,
                response_time=response_time,
                message=f"Database connection failed: {str(e)}",
                details={"error": str(e)}
            )
    
    async def _check_llm_health(self) -> ComponentHealth:
        """Check LLM service health."""
        start_time = time.time()
        
        try:
            # Simulate LLM health check
            # In real implementation, this would check LLM API availability
            await self._simulate_llm_call()
            
            response_time = time.time() - start_time
            
            return ComponentHealth(
                name="llm_service",
                status=HealthStatus.HEALTHY,
                response_time=response_time,
                message="LLM service available",
                details={"model": "llama-3.3-70b-versatile", "response_time": response_time}
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            
            return ComponentHealth(
                name="llm_service",
                status=HealthStatus.UNHEALTHY,
                response_time=response_time,
                message=f"LLM service unavailable: {str(e)}",
                details={"error": str(e)}
            )
    
    async def _check_cache_health(self) -> ComponentHealth:
        """Check cache component health."""
        start_time = time.time()
        
        try:
            # Simulate cache health check
            # In real implementation, this would check Redis connection
            await self._simulate_cache_operation()
            
            response_time = time.time() - start_time
            
            return ComponentHealth(
                name="cache",
                status=HealthStatus.HEALTHY,
                response_time=response_time,
                message="Cache service available",
                details={"type": "redis", "hit_rate": 0.85, "response_time": response_time}
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            
            return ComponentHealth(
                name="cache",
                status=HealthStatus.DEGRADED,
                response_time=response_time,
                message=f"Cache service degraded: {str(e)}",
                details={"error": str(e)}
            )
    
    async def _check_filesystem_health(self) -> ComponentHealth:
        """Check file system health."""
        start_time = time.time()
        
        try:
            # Check disk space and file accessibility
            disk_usage = psutil.disk_usage('/')
            free_space_percent = (disk_usage.free / disk_usage.total) * 100
            
            response_time = time.time() - start_time
            
            # Determine status based on free space
            if free_space_percent < 10:
                status = HealthStatus.CRITICAL
                message = "Critically low disk space"
            elif free_space_percent < 20:
                status = HealthStatus.DEGRADED
                message = "Low disk space"
            else:
                status = HealthStatus.HEALTHY
                message = "File system healthy"
            
            return ComponentHealth(
                name="filesystem",
                status=status,
                response_time=response_time,
                message=message,
                details={
                    "free_space_gb": disk_usage.free / (1024**3),
                    "total_space_gb": disk_usage.total / (1024**3),
                    "free_space_percent": free_space_percent
                }
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            
            return ComponentHealth(
                name="filesystem",
                status=HealthStatus.UNHEALTHY,
                response_time=response_time,
                message=f"File system check failed: {str(e)}",
                details={"error": str(e)}
            )
    
    async def _check_system_resources_health(self) -> ComponentHealth:
        """Check system resources health."""
        start_time = time.time()
        
        try:
            # Get system metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            response_time = time.time() - start_time
            
            # Determine status based on resource usage
            if cpu_percent > 90 or memory.percent > 90:
                status = HealthStatus.CRITICAL
                message = "Critical resource usage"
            elif cpu_percent > 80 or memory.percent > 80:
                status = HealthStatus.DEGRADED
                message = "High resource usage"
            else:
                status = HealthStatus.HEALTHY
                message = "System resources healthy"
            
            return ComponentHealth(
                name="system_resources",
                status=status,
                response_time=response_time,
                message=message,
                details={
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory.percent,
                    "memory_available_gb": memory.available / (1024**3)
                }
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            
            return ComponentHealth(
                name="system_resources",
                status=HealthStatus.UNHEALTHY,
                response_time=response_time,
                message=f"System resource check failed: {str(e)}",
                details={"error": str(e)}
            )
    
    def _determine_overall_health(self, components: List[ComponentHealth]) -> HealthStatus:
        """Determine overall system health from component health."""
        if any(comp.status == HealthStatus.CRITICAL for comp in components):
            return HealthStatus.CRITICAL
        elif any(comp.status == HealthStatus.UNHEALTHY for comp in components):
            return HealthStatus.UNHEALTHY
        elif any(comp.status == HealthStatus.DEGRADED for comp in components):
            return HealthStatus.DEGRADED
        else:
            return HealthStatus.HEALTHY
    
    # Simulation methods (replace with real implementations)
    async def _simulate_database_query(self) -> None:
        """Simulate database query for health check."""
        # In real implementation, this would execute a simple query
        await asyncio.sleep(0.01)  # Simulate query time
    
    async def _simulate_llm_call(self) -> None:
        """Simulate LLM API call for health check."""
        # In real implementation, this would make a simple LLM API call
        await asyncio.sleep(0.05)  # Simulate API call time
    
    async def _simulate_cache_operation(self) -> None:
        """Simulate cache operation for health check."""
        # In real implementation, this would perform a cache get/set operation
        await asyncio.sleep(0.005)  # Simulate cache operation time


# Add asyncio import for simulation methods
import asyncio
