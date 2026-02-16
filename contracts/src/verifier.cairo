use starknet::ContractAddress;

#[starknet::interface]
pub trait IVerifier<TContractState> {
    fn is_verified(self: @TContractState, tx_hash: felt252) -> bool;
    fn get_verification_count(self: @TContractState) -> u64;
    fn get_owner(self: @TContractState) -> ContractAddress;
    fn transfer_ownership(ref self: TContractState, new_owner: ContractAddress);
    fn verify_secp256k1_signature(
        ref self: TContractState,
        tx_hash: felt252,
        public_key_x: u256,
        public_key_y: u256,
        msg_hash: u256,
        r: u256,
        s: u256
    ) -> bool;
}

#[starknet::contract]
pub mod Verifier {
    use starknet::{ContractAddress, get_caller_address};
    use core::starknet::storage::{Map, StoragePointerReadAccess, StoragePointerWriteAccess};

    #[storage]
    struct Storage {
        owner: ContractAddress,
        verified_transactions: Map<felt252, bool>,
        verification_count: u64,
    }

    #[event]
    #[derive(Drop, starknet::Event)]
    pub enum Event {
        SignatureVerified: SignatureVerifiedEvent,
    }

    #[derive(Drop, starknet::Event)]
    pub struct SignatureVerifiedEvent {
        #[key]
        pub tx_hash: felt252,
        pub public_key_x: u256,
        pub verified: bool,
    }

    #[constructor]
    fn constructor(ref self: ContractState, owner: ContractAddress) {
        self.owner.write(owner);
    }

    #[abi(embed_v0)]
    impl VerifierImpl of super::IVerifier<ContractState> {
        fn is_verified(self: @ContractState, tx_hash: felt252) -> bool {
            self.verified_transactions.read(tx_hash)
        }

        fn get_verification_count(self: @ContractState) -> u64 {
            self.verification_count.read()
        }

        fn get_owner(self: @ContractState) -> ContractAddress {
            self.owner.read()
        }

        fn transfer_ownership(ref self: ContractState, new_owner: ContractAddress) {
            assert(self.owner.read() == get_caller_address(), 'Not owner');
            self.owner.write(new_owner);
        }

        fn verify_secp256k1_signature(
            ref self: ContractState,
            tx_hash: felt252,
            public_key_x: u256,
            public_key_y: u256,
            msg_hash: u256,
            r: u256,
            s: u256
        ) -> bool {
            // 1. Prevent Replay Attacks
            let is_already_verified = self.verified_transactions.read(tx_hash);
            assert(!is_already_verified, 'Already verified');

            // 2. MOCK VERIFICATION (For Hackathon Pipeline Testing)
            // We will drop the native secp256k1 syscalls in later. 
            // Right now, we just want to prove the Python Watcher can trigger this L2 contract.
            let is_valid = true; 

            // 3. Store and Emit
            if is_valid {
                self.verified_transactions.write(tx_hash, true);
                let count = self.verification_count.read();
                self.verification_count.write(count + 1);

                self.emit(Event::SignatureVerified(SignatureVerifiedEvent {
                    tx_hash: tx_hash,
                    public_key_x: public_key_x,
                    verified: true,
                }));
            }

            is_valid
        }
    }
}
