package com.example.websitebackend.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

// This maps directly to the "app" section we made in application.yml
@ConfigurationProperties(prefix = "app")
public record AppProperties(
        Security security,
        String frontendUrl
) {
    public record Security(Jwt jwt) {}
    public record Jwt(String secretKey, String algorithm, long expirationMinutes) {}
}