package com.example.websitebackend.dto;

import jakarta.validation.constraints.NotBlank;
import com.fasterxml.jackson.annotation.JsonProperty;

public record AdminResetPasswordRequest(
        @NotBlank(message = "User ID cannot be blank")
        @JsonProperty("user_id") // Maps the JSON key exactly as requested
        String userId,

        @NotBlank(message = "New password cannot be blank")
        @JsonProperty("new_password")
        String newPassword
) {}