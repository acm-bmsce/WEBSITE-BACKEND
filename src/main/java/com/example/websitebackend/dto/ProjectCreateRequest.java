package com.example.websitebackend.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;
import java.util.List;

@Data
public class ProjectCreateRequest {
    @NotBlank(message = "Title is required")
    private String title;

    @NotBlank(message = "Description is required")
    private String description;

    @NotBlank(message = "Author is required")
    private String author;

    private String githubUrl;
    private String imageUrl;

    private List<String> categories;
    private List<String> techStack;

    private String status;
}