package com.example.websitebackend.repository;

import com.example.websitebackend.model.Insight;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface InsightRepository extends MongoRepository<Insight, String> {
    // No custom methods needed! findAll(Pageable) is built-in.
}