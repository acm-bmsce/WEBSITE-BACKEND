package com.example.websitebackend.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import java.util.List;

@Data
public class EventUpdateRequest {
    private String title;
    private String description;
    @JsonProperty("date_str")
    private String dateStr;
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