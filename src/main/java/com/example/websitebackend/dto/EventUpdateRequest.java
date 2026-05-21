package com.example.websitebackend.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import java.util.Date;
import java.util.List;

@Data
public class EventUpdateRequest {
    // Everything is optional in an update request, so no @NotBlank or @NotNull annotations
    private String title;

    private String description;

    private Date date; // ✅ Lombok generates getDate() from this

    private String image;

    private String fullDescription;

    private String outcomes;

    private List<String> gallery;

    private String location;

    private Integer attendees;

    @JsonProperty("registration_link")
    private String registrationLink;

    @JsonProperty("is_featured")
    private Boolean isFeatured;
}