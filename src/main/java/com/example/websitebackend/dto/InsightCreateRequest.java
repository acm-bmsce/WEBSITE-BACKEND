package com.example.websitebackend.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class InsightCreateRequest {
    @NotBlank(message = "Person name is required")
    private String personName;

    @NotBlank(message = "Description is required")
    private String description;

    private String image;

    @JsonProperty("insta_link")
    private String instaLink;

    private String title;
    private String bgColor;
    private String borderColor;
    private String size;
    private String year;
}