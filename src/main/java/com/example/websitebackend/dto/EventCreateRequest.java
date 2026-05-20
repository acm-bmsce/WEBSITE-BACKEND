package com.example.websitebackend.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;
import java.util.List;

@Data
public class EventCreateRequest {
    @NotBlank(message = "Title is required")
    private String title;

    @NotBlank(message = "Description is required")
    private String description;

    @NotBlank(message = "Date string is required")
    @JsonProperty("date_str")
    private String dateStr;

    private String image;

    @NotBlank(message = "Full description is required")
    private String fullDescription;

    private String outcomes;
    private List<String> gallery;
    private String location;
    private String attendees; // String or Int in Python, we'll parse it as String first

    @JsonProperty("registration_link")
    private String registrationLink;

    @JsonProperty("is_featured")
    private boolean isFeatured;
}