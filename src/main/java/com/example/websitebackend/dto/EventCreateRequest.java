package com.example.websitebackend.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

import java.util.Date;
import java.util.List;

@Data
public class EventCreateRequest {
    @NotBlank(message = "Title is required")
    private String title;

    @NotBlank(message = "Description is required")
    private String description;

    @NotNull(message = "Date is required")
    private Date date; // ✅ Lombok generates getDate() from this

    private String image;

    @NotBlank(message = "Full description is required")
    private String fullDescription;

    private String outcomes;

    private List<String> gallery;

    private String location;

    private Integer attendees;

    @JsonProperty("registration_link")
    private String registrationLink;

    @JsonProperty("is_featured")
    private boolean isFeatured;
}