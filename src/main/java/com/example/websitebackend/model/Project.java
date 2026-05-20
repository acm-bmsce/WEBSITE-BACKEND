package com.example.websitebackend.model;

import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Data
@Document(collection = "projects")
public class Project {

    @Id
    private String id;

    private String title;
    private String description;

    // We keep the exact naming you used for the frontend
    private String author;
    private String githubUrl;
    private String imageUrl;

    private List<String> categories = new ArrayList<>();
    private List<String> techStack = new ArrayList<>();

    private String status = "PENDING";

    // Spring Data MongoDB can handle defaults via standard Java instantiation
    private LocalDateTime submissionDate = LocalDateTime.now();
}