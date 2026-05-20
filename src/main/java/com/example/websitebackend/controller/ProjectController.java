package com.example.websitebackend.controller;

import com.example.websitebackend.dto.ProjectCreateRequest;
import com.example.websitebackend.model.Project;
import com.example.websitebackend.service.ProjectService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/projects")
@RequiredArgsConstructor
public class ProjectController {

    private final ProjectService projectService;

    @PostMapping
    public ResponseEntity<Project> createProject(@Valid @RequestBody ProjectCreateRequest request) {
        Project newProject = projectService.createProject(request);
        return new ResponseEntity<>(newProject, HttpStatus.CREATED);
    }

    @GetMapping("/showcase")
    public ResponseEntity<List<Project>> getPublicProjects(
            @RequestParam(defaultValue = "20") int limit,
            @RequestParam(defaultValue = "0") int skip
    ) {
        Page<Project> projects = projectService.getPublicProjects(skip, limit);
        return ResponseEntity.ok(projects.getContent());
    }

    @GetMapping
    public ResponseEntity<List<Project>> getAllProjects(
            @RequestParam(defaultValue = "20") int limit,
            @RequestParam(defaultValue = "0") int skip
    ) {
        Page<Project> projects = projectService.getAllProjects(skip, limit);
        return ResponseEntity.ok(projects.getContent());
    }

     @PreAuthorize("hasRole('MASTER', 'COORDINATOR')")
    @PatchMapping("/{projectId}")
    public ResponseEntity<Project> updateProject(
            @PathVariable String projectId,
            @RequestBody ProjectCreateRequest request
    ) {
        Project updatedProject = projectService.updateProject(projectId, request);
        return ResponseEntity.ok(updatedProject);
    }

     @PreAuthorize("hasRole('MASTER')")
    @PatchMapping("/{projectId}/approve")
    public ResponseEntity<Map<String, Object>> approveProject(@PathVariable String projectId) {
        Project approvedProject = projectService.approveProject(projectId);
        return ResponseEntity.ok(Map.of(
                "message", "Project approved successfully",
                "project", approvedProject
        ));
    }

     @PreAuthorize("hasRole('MASTER')")
    @DeleteMapping("/{projectId}")
    public ResponseEntity<Map<String, String>> deleteProject(@PathVariable String projectId) {
        projectService.deleteProject(projectId);
        return ResponseEntity.ok(Map.of("message", "Project deleted successfully"));
    }
}