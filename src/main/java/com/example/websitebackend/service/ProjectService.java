package com.example.websitebackend.service;

import com.example.websitebackend.dto.ProjectCreateRequest;
import com.example.websitebackend.model.Project;
import com.example.websitebackend.repository.ProjectRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class ProjectService {

    private final ProjectRepository projectRepository;

    public Project createProject(ProjectCreateRequest request) {
        Project project = new Project();
        project.setTitle(request.getTitle());
        project.setDescription(request.getDescription());
        project.setAuthor(request.getAuthor());
        project.setGithubUrl(request.getGithubUrl());
        project.setImageUrl(request.getImageUrl());

        if (request.getCategories() != null) project.setCategories(request.getCategories());
        if (request.getTechStack() != null) project.setTechStack(request.getTechStack());

        // Handle default status
        if (request.getStatus() != null && !request.getStatus().trim().isEmpty()) {
            project.setStatus(request.getStatus());
        } else {
            project.setStatus("PENDING");
        }

        return projectRepository.save(project);
    }

    public Page<Project> getPublicProjects(int skip, int limit) {
        int page = skip / limit;
        Pageable pageable = PageRequest.of(page, limit, Sort.by(Sort.Direction.DESC, "submissionDate"));
        return projectRepository.findByStatus("APPROVED", pageable);
    }

    public Page<Project> getAllProjects(int skip, int limit) {
        int page = skip / limit;
        Pageable pageable = PageRequest.of(page, limit, Sort.by(Sort.Direction.DESC, "submissionDate"));
        return projectRepository.findAll(pageable);
    }

    public Project updateProject(String projectId, ProjectCreateRequest request) {
        Project project = projectRepository.findById(projectId)
                .orElseThrow(() -> new IllegalArgumentException("Project not found"));

        // Partial update logic
        if (request.getTitle() != null) project.setTitle(request.getTitle());
        if (request.getDescription() != null) project.setDescription(request.getDescription());
        if (request.getAuthor() != null) project.setAuthor(request.getAuthor());
        if (request.getGithubUrl() != null) project.setGithubUrl(request.getGithubUrl());
        if (request.getImageUrl() != null) project.setImageUrl(request.getImageUrl());
        if (request.getCategories() != null) project.setCategories(request.getCategories());
        if (request.getTechStack() != null) project.setTechStack(request.getTechStack());
        if (request.getStatus() != null) project.setStatus(request.getStatus());

        return projectRepository.save(project);
    }

    public Project approveProject(String projectId) {
        Project project = projectRepository.findById(projectId)
                .orElseThrow(() -> new IllegalArgumentException("Project not found"));

        project.setStatus("APPROVED");
        return projectRepository.save(project);
    }

    public void deleteProject(String projectId) {
        if (!projectRepository.existsById(projectId)) {
            throw new IllegalArgumentException("Project not found");
        }
        projectRepository.deleteById(projectId);
    }
}