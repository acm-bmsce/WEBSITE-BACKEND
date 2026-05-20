package com.example.websitebackend.repository;

import com.example.websitebackend.model.Event;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface EventRepository extends MongoRepository<Event, String> {

    // Spring automatically handles finding by featured status and applying pagination/sorting
    Page<Event> findByIsFeatured(boolean isFeatured, Pageable pageable);
}