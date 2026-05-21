package com.example.websitebackend.config;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.lang.NonNull;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;

@Component // Tells Spring to automatically register this filter
public class RequestLoggingFilter extends OncePerRequestFilter {

    // Create a logger for this class
    private static final Logger logger = LoggerFactory.getLogger(RequestLoggingFilter.class);

    @Override
    protected void doFilterInternal(
            @NonNull HttpServletRequest request,
            @NonNull HttpServletResponse response,
            @NonNull FilterChain filterChain
    ) throws ServletException, IOException {

        // 1. Record the start time
        long startTime = System.currentTimeMillis();

        // 2. Let the request continue to the controller (or security chain)
        filterChain.doFilter(request, response);

        // 3. Calculate how long it took
        long duration = System.currentTimeMillis() - startTime;

        // 4. Log it FastAPI style! (e.g., "GET /api/events" 200 in 15ms)
        logger.info("\"{} {}\" {} in {}ms",
                request.getMethod(),
                request.getRequestURI(),
                response.getStatus(),
                duration);
    }
}