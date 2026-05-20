package com.example.websitebackend.repository;

import com.example.websitebackend.model.Project;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ProjectRepository extends MongoRepository<Project, String> {

    // Equivalent to Project.find(Project.status == "APPROVED") in Python
    Page<Project> findByStatus(String status, Pageable pageable);
}