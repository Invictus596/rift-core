mod verifier;

#[cfg(test)]
mod tests {
    use garaga::ec::EcPoint;

    #[test]
    fn test_garaga_import() {
        // This test confirms that the Garaga library is properly imported
        // and accessible in our project
        assert(true, 'Garaga import successful');
    }
}