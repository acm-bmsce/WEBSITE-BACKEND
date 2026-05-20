package com.example.websitebackend.controller;

import com.example.websitebackend.dto.AdminResetPasswordRequest;
import com.example.websitebackend.dto.UserCreateRequest;
import com.example.websitebackend.model.User;
import com.example.websitebackend.service.UserService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/users") // Base path for all routes in this controller
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    // --- AUTH ROUTES ---

    @PostMapping("/register")
    public ResponseEntity<User> register(@Valid @RequestBody UserCreateRequest request) {
        User newUser = userService.registerUser(request);
        return new ResponseEntity<>(newUser, HttpStatus.CREATED);
    }

    // Note: The /login endpoint is usually handled automatically by Spring Security filters.
    // We will build a custom login endpoint in Phase 5.

    // --- ADMIN MANAGEMENT ROUTES ---

    @GetMapping("/pending")
    @PreAuthorize("hasRole('MASTER')")
    public ResponseEntity<List<User>> getPendingUsers() {
        return ResponseEntity.ok(userService.getPendingUsers());
    }

    @PreAuthorize("hasRole('MASTER')")
    @PatchMapping("/{userId}/approve")
    public ResponseEntity<Map<String, String>> approveUser(@PathVariable String userId) {
        userService.approveUser(userId);
        return ResponseEntity.ok(Map.of("message", "User approved."));
    }

    // --- PASSWORD RESET FLOW ---

    @PostMapping("/request-reset")
    public ResponseEntity<Map<String, String>> requestPasswordReset(@RequestParam String username) {
        userService.requestPasswordReset(username);
        return ResponseEntity.ok(Map.of("message", "Request sent to Master Admin."));
    }

    @GetMapping("/reset-requests")
    public ResponseEntity<List<User>> getResetRequests() {
        return ResponseEntity.ok(userService.getResetRequests());
    }

    @PostMapping("/approve-reset")
    public ResponseEntity<Map<String, String>> approveResetPassword(@Valid @RequestBody AdminResetPasswordRequest request) {
        userService.approveResetPassword(request);
        return ResponseEntity.ok(Map.of("message", "Password reset successfully."));
    }
}