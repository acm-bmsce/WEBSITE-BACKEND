package com.example.websitebackend.repository;

import com.example.websitebackend.model.User;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface UserRepository extends MongoRepository<User, String> {

    // Spring automatically knows to generate a query like:
    // db.users.findOne({ "email": email })
    Optional<User> findByEmail(String email);

    // Spring automatically knows how to find by username
    Optional<User> findByUsername(String username);

    List<User> findByIsApprovedFalse();
    List<User> findByResetRequestedTrue();
}