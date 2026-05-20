package com.example.websitebackend.service;

import com.example.websitebackend.dto.AdminResetPasswordRequest;
import com.example.websitebackend.dto.UserCreateRequest;
import com.example.websitebackend.model.User;
import com.example.websitebackend.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    // We will configure the actual PasswordEncoder bean in Phase 5 (Security)
    private final PasswordEncoder passwordEncoder;

    public User registerUser(UserCreateRequest request) {
        if (userRepository.findByUsername(request.username()).isPresent()) {
            throw new RuntimeException("Username already registered"); // We'll handle custom exceptions later
        }
        if (userRepository.findByEmail(request.email()).isPresent()) {
            throw new RuntimeException("Email already registered");
        }

        User newUser = new User();
        newUser.setUsername(request.username());
        newUser.setEmail(request.email());
        newUser.setHashedPassword(passwordEncoder.encode(request.password()));
        newUser.setApproved(false);
        // role defaults to "coordinator" in the User entity

        return userRepository.save(newUser);
    }

    public List<User> getPendingUsers() {
        // We'll create this custom query method in the repository in a moment
        return userRepository.findByIsApprovedFalse();
    }

    public void approveUser(String userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));
        user.setApproved(true);
        userRepository.save(user);
    }

    public void requestPasswordReset(String username) {
        Optional<User> userOpt = userRepository.findByUsername(username);
        if (userOpt.isPresent()) {
            User user = userOpt.get();
            user.setResetRequested(true);
            userRepository.save(user);
        }
        // Security: Fail silently if user doesn't exist, just like your Python code
    }

    public List<User> getResetRequests() {
        return userRepository.findByResetRequestedTrue();
    }

    public void approveResetPassword(AdminResetPasswordRequest request) {
        User user = userRepository.findById(request.userId())
                .orElseThrow(() -> new RuntimeException("User not found"));

        user.setHashedPassword(passwordEncoder.encode(request.newPassword()));
        user.setResetRequested(false);
        userRepository.save(user);
    }
}